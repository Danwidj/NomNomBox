"use client";

import type React from "react";
import { useEffect, useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Calendar } from "@/components/ui/calendar";
import { Plus, Trash2, CalendarIcon, Copy, Clock } from "lucide-react";
import {
  format,
  fromUnixTime,
  getUnixTime,
  startOfDay,
  endOfDay,
} from "date-fns";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import type { DateRange } from "react-day-picker";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import axios from "axios";

type TimeSlot = {
  start: number; // Unix timestamp
  end: number; // Unix timestamp
  isExisting?: boolean; // Flag to identify if this is an existing timeslot from the backend
  id?: number; // ID to track timeslots for deletion
};

type DateSchedule = {
  date: number; // Unix timestamp (start of day)
  timeSlots: TimeSlot[];
};

// Generate time options in Unix format (seconds since epoch)
// These are offsets from the start of day (in seconds) from 08:00 to 22:00 in one-hour increments
const TIME_OFFSETS = Array.from({ length: 15 }, (_, i) => {
  const hour = i + 8; // Start from 8 (8 AM) and go up to 22 (10 PM)
  return hour * 3600; // Convert to seconds (1 hour = 3600 seconds)
});

export default function DateBasedDriverSchedule() {
  const [existingSchedule, setExistingSchedule] = useState<DateSchedule[]>([]);
  const [newSchedule, setNewSchedule] = useState<DateSchedule[]>([]);
  const [dateRange, setDateRange] = useState<DateRange | undefined>();
  const [activeTab, setActiveTab] = useState<string>("existing");

  // Store original existing timeslots to track deletions
  const originalTimeslots = useRef<number[]>([]);
  const deletedTimeslots = useRef<Set<number>>(new Set()); // Using Set to avoid duplicates

  // Common time slots as offsets from start of day (in seconds)
  const [commonTimeSlots, setCommonTimeSlots] = useState<TimeSlot[]>([
    { start: 8 * 3600, end: 12 * 3600 }, // 8:00 - 12:00
    { start: 13 * 3600, end: 17 * 3600 }, // 13:00 - 17:00
  ]);

  // Fetch data
  useEffect(() => {
    const driver_id = localStorage.getItem("driver_id") || "1";

    // Mock data instead of making an API call with undefined URL
    const mockTimeslots = [
      Math.floor(Date.now() / 1000), // Current time in Unix
      Math.floor(Date.now() / 1000) + 3600, // 1 hour later
      Math.floor(Date.now() / 1000) + 86400, // Tomorrow same time
      Math.floor(Date.now() / 1000) + 86400 + 3600, // Tomorrow 1 hour later
    ];

    // Store original timeslots for tracking deletions
    originalTimeslots.current = [...mockTimeslots];

    const convertedSchedule = groupTimeSlotsByDate(mockTimeslots, true);
    setExistingSchedule(convertedSchedule);

    // If you need to make an actual API call, uncomment and provide a valid URL:

    axios
      .get(
        `https://personal-6fbyxkeb.outsystemscloud.com/Driver/rest/DriverAPI/drivers/${driver_id}/timeslots`
      )
      .then((response) => {
        console.log(response.data.timeslots);
        originalTimeslots.current = [...response.data.timeslots];
        const convertedSchedule = groupTimeSlotsByDate(
          response.data.timeslots,
          true
        );
        setExistingSchedule(convertedSchedule);
      })
      .catch((error) => {
        console.error("Error fetching schedule:", error);
        toast.error("Failed to load schedule");
      });
  }, []);

  // Group time slots by date
  const groupTimeSlotsByDate = (timeSlots: number[], isExisting = false) => {
    const groupedByDate: Record<number, TimeSlot[]> = {};

    // Filter out deleted timeslots
    const filteredTimeSlots = timeSlots.filter(
      (ts) => !deletedTimeslots.current.has(ts)
    );

    filteredTimeSlots.forEach((startTime) => {
      const endTime = startTime + 3600; // 1 hour slot (3600 seconds)
      const dateTimestamp = getStartOfDayUnix(startTime);

      if (!groupedByDate[dateTimestamp]) {
        groupedByDate[dateTimestamp] = [];
      }

      groupedByDate[dateTimestamp].push({
        start: startTime,
        end: endTime,
        isExisting,
        id: startTime, // Use the start time as the ID
      });
    });

    return Object.entries(groupedByDate).map(([dateStr, slots]) => ({
      date: Number.parseInt(dateStr),
      timeSlots: slots,
    }));
  };

  // Helper to get start of day in Unix time
  const getStartOfDayUnix = (timestamp: number) => {
    return getUnixTime(startOfDay(fromUnixTime(timestamp)));
  };

  // Helper to get end of day in Unix time
  const getEndOfDayUnix = (timestamp: number) => {
    return getUnixTime(endOfDay(fromUnixTime(timestamp)));
  };

  // Helper to format Unix time as HH:MM
  const formatUnixToTime = (unix: number) => {
    if (!unix) return "00:00";
    try {
      return format(fromUnixTime(unix), "HH:mm");
    } catch (error) {
      console.error("Error formatting unix time:", error);
      return "00:00";
    }
  };

  // Helper to format offset seconds as HH:MM
  const formatOffsetToTime = (offsetSeconds: number) => {
    try {
      const hours = Math.floor(offsetSeconds / 3600);
      const minutes = Math.floor((offsetSeconds % 3600) / 60);
      return `${hours.toString().padStart(2, "0")}:${minutes
        .toString()
        .padStart(2, "0")}`;
    } catch (error) {
      console.error("Error formatting offset seconds:", error);
      return "00:00";
    }
  };

  // Helper to convert day offset seconds to Unix timestamp
  const offsetToUnixTime = (dateUnix: number, offsetSeconds: number) => {
    return dateUnix + offsetSeconds;
  };

  // Helper to get time offset from Unix timestamp relative to its day start
  const getTimeOffsetFromUnix = (unix: number) => {
    try {
      const dayStart = getStartOfDayUnix(unix);
      return unix - dayStart;
    } catch (error) {
      console.error("Error getting time offset:", error);
      return 0;
    }
  };

  const addDateRange = () => {
    if (dateRange?.from) {
      const fromUnix = getUnixTime(startOfDay(dateRange.from));
      // If to is not defined, use from date as the to date (single date selection)
      const toUnix = dateRange.to
        ? getUnixTime(startOfDay(dateRange.to))
        : fromUnix;

      // Generate array of days between from and to
      const days = [];
      let currentDay = fromUnix;

      while (currentDay <= toUnix) {
        days.push(currentDay);
        currentDay += 86400; // Add one day in seconds
      }

      // Filter out days that are already in the schedule
      const newDays = days.filter(
        (day) => !newSchedule.some((item) => item.date === day)
      );

      if (newDays.length > 0) {
        setNewSchedule((prev) => [
          ...prev,
          ...newDays.map((day) => ({
            date: day,
            timeSlots: [],
          })),
        ]);
        setDateRange(undefined);
        toast.success("Dates added", {
          description: `Added ${newDays.length} new date(s) to your schedule.`,
        });
      } else {
        toast.info("No new dates added", {
          description: "All selected dates are already in your schedule.",
        });
      }
    }
  };

  const removeDate = (date: number) => {
    setNewSchedule((prev) => prev.filter((item) => item.date !== date));
  };

  // Update the removeExistingTimeSlot function to properly track deleted timeslots
  const removeExistingTimeSlot = (date: number, index: number) => {
    setExistingSchedule((prev) => {
      // Get the timeslot to be removed
      const timeslot = prev.find((item) => item.date === date)?.timeSlots[
        index
      ];

      // If it's an original timeslot, add it to the deletedTimeslots set
      if (
        timeslot &&
        timeslot.id &&
        originalTimeslots.current.includes(timeslot.id)
      ) {
        deletedTimeslots.current.add(timeslot.id);
      }

      // Filter out the deleted timeslot
      return prev
        .map((item) =>
          item.date === date
            ? {
                ...item,
                timeSlots: item.timeSlots.filter((_, i) => i !== index),
              }
            : item
        )
        .filter((item) => item.timeSlots.length > 0); // Remove dates with no timeslots
    });
  };

  const addTimeSlot = (date: number) => {
    setNewSchedule((prev) =>
      prev.map((item) =>
        item.date === date
          ? {
              ...item,
              timeSlots: [
                ...item.timeSlots,
                {
                  start: offsetToUnixTime(date, 8 * 3600), // 8:00 AM
                  end: offsetToUnixTime(date, 9 * 3600), // 9:00 AM
                },
              ],
            }
          : item
      )
    );
  };

  const removeTimeSlot = (date: number, index: number) => {
    setNewSchedule(
      (prev) =>
        prev
          .map((item) =>
            item.date === date
              ? {
                  ...item,
                  timeSlots: item.timeSlots.filter((_, i) => i !== index),
                }
              : item
          )
          .filter((item) => item.timeSlots.length > 0) // Remove dates with no timeslots
    );
  };

  const updateTimeSlot = (
    date: number,
    index: number,
    field: "start" | "end",
    offsetSeconds: number
  ) => {
    setNewSchedule((prev) =>
      prev.map((item) =>
        item.date === date
          ? {
              ...item,
              timeSlots: item.timeSlots.map((slot, i) =>
                i === index
                  ? {
                      ...slot,
                      [field]: offsetToUnixTime(date, offsetSeconds),
                    }
                  : slot
              ),
            }
          : item
      )
    );
  };

  const addCommonTimeSlot = () => {
    setCommonTimeSlots((prev) => [
      ...prev,
      {
        start: 8 * 3600, // 8:00 AM offset
        end: 9 * 3600, // 9:00 AM offset
      },
    ]);
  };

  const removeCommonTimeSlot = (index: number) => {
    setCommonTimeSlots((prev) => prev.filter((_, i) => i !== index));
  };

  const updateCommonTimeSlot = (
    index: number,
    field: "start" | "end",
    offsetSeconds: number
  ) => {
    setCommonTimeSlots((prev) =>
      prev.map((slot, i) =>
        i === index ? { ...slot, [field]: offsetSeconds } : slot
      )
    );
  };

  const applyCommonTimeSlotsToAll = () => {
    // Validate common time slots
    for (let index = 0; index < commonTimeSlots.length; index++) {
      const item = commonTimeSlots[index];
      if (item.start >= item.end) {
        toast.warning("Invalid Time Slot", {
          description: "Start time must be before end time.",
        });
        return;
      }

      const otherTimeSlots = commonTimeSlots.filter((_, i) => i !== index);
      if (!isValidTimeSlot(otherTimeSlots, item.start, item.end)) {
        toast.warning("Invalid Time Slot", {
          description: "Time slots cannot overlap.",
        });
        return;
      }
    }

    // Apply common time slots to all dates
    setNewSchedule((prev) =>
      prev.map((item) => ({
        ...item,
        timeSlots: commonTimeSlots.map((slot) => ({
          start: offsetToUnixTime(item.date, slot.start),
          end: offsetToUnixTime(item.date, slot.end),
        })),
      }))
    );

    toast.success("Common Time Slots Applied", {
      description: "Applied common time slots to all dates in your schedule.",
    });
  };

  const applyCommonTimeSlotsToDate = (date: number) => {
    setNewSchedule((prev) =>
      prev.map((item) =>
        item.date === date
          ? {
              ...item,
              timeSlots: commonTimeSlots.map((slot) => ({
                start: offsetToUnixTime(date, slot.start),
                end: offsetToUnixTime(date, slot.end),
              })),
            }
          : item
      )
    );

    toast.success("Common Time Slots Applied", {
      description: `Applied common time slots to ${format(
        fromUnixTime(date),
        "MMMM d, yyyy"
      )}.`,
    });
  };

  // Update the handleSubmit function to properly handle deleted timeslots
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Get driver id from local storage
    const driverId = Number.parseInt(localStorage.getItem("driver_id") || "1");

    // Prepare changes array for submission
    const changes = [];

    // Add deleted timeslots to changes
    for (const timeslotId of deletedTimeslots.current) {
      changes.push({
        timeslot: timeslotId,
        change_type: "delete",
      });
    }

    // Add new timeslots to changes
    // const addedTimeslots = [];
    // for (const dateSchedule of newSchedule) {
    //   for (const slot of dateSchedule.timeSlots) {
    //     changes.push({
    //       timeslot: slot.start,
    //       change_type: "add",
    //     });
    //     addedTimeslots.push(slot.start);
    //   }
    // }

    const addedTimeslots = [];
    for (const dateSchedule of newSchedule) {
      for (const slot of dateSchedule.timeSlots) {
        for (let time = slot.start; time < slot.end; time += 3600) {
          // Increment by 1 hour (3600 seconds)
          changes.push({
            timeslot: time,
            change_type: "add",
          });
          addedTimeslots.push(time);
        }
      }
    }

    const submittedData = {
      driver_id: driverId,
      changes: changes,
    };

    console.log("Submitted data:", submittedData);

    // Move new timeslots to existing timeslots
    if (newSchedule.length > 0) {
      // Convert new schedule to existing format
      const newAsExisting = newSchedule.map((dateSchedule) => ({
        ...dateSchedule,
        timeSlots: dateSchedule.timeSlots.map((slot) => ({
          ...slot,
          isExisting: true,
          id: slot.start,
        })),
      }));

      // Merge with existing schedule
      setExistingSchedule((prev) => {
        const merged = [...prev];

        // For each date in new schedule
        newAsExisting.forEach((newDateSchedule) => {
          // Check if this date already exists in existing schedule
          const existingDateIndex = merged.findIndex(
            (item) => item.date === newDateSchedule.date
          );

          if (existingDateIndex >= 0) {
            // Add timeslots to existing date
            merged[existingDateIndex] = {
              ...merged[existingDateIndex],
              timeSlots: [
                ...merged[existingDateIndex].timeSlots,
                ...newDateSchedule.timeSlots,
              ],
            };
          } else {
            // Add new date with timeslots
            merged.push(newDateSchedule);
          }
        });

        return merged;
      });

      // Add new timeslots to originalTimeslots
      originalTimeslots.current = [
        ...originalTimeslots.current,
        ...addedTimeslots,
      ];

      // Clear new schedule
      setNewSchedule([]);
    }

    // Reset the changes tracking after submission
    deletedTimeslots.current.clear();

    toast.success("Schedule Updated", {
      description:
        "Your flexible working schedule has been successfully updated.",
    });

    // Switch to existing tab
    setActiveTab("existing");

    // In a real implementation, you would reset the changes array after a successful API call:
    const endpoint = "http://localhost:5000/availability";
    axios
      .post(endpoint, submittedData)
      .then((response) => {
        // Clear the changes tracking after successful submission
        console.log(response.data);
        deletedTimeslots.current.clear();

        toast.success("Schedule Updated", {
          description:
            "Your flexible working schedule has been successfully updated.",
        });

        // Switch to existing tab
        setActiveTab("existing");
      })
      .catch((error) => {
        console.error("Error updating schedule:", error);
        toast.error("Failed to update schedule");
      });
  };

  const isValidTimeSlot = (
    timeslots: TimeSlot[],
    start: number,
    end: number
  ) => {
    if (start >= end) {
      return false;
    }

    if (timeslots.length === 0) {
      return true;
    }

    for (const timeslot of timeslots) {
      // Check if the new slot overlaps with any existing slot
      if (
        (start >= timeslot.start && start < timeslot.end) ||
        (end > timeslot.start && end <= timeslot.end) ||
        (start <= timeslot.start && end >= timeslot.end)
      ) {
        return false;
      }
    }

    return true;
  };

  // Sort schedule by date
  const sortedExistingSchedule = [...existingSchedule].sort(
    (a, b) => a.date - b.date
  );
  const sortedNewSchedule = [...newSchedule].sort((a, b) => a.date - b.date);

  return (
    <div className="container mx-auto px-4 py-6 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6 text-center">
        Set Your Flexible Working Schedule
      </h1>
      <form onSubmit={handleSubmit}>
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Common Time Slots</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {commonTimeSlots.map((slot, index) => (
                <div key={index} className="flex items-center space-x-4">
                  <div className="grid gap-2">
                    <Label htmlFor={`common-start-${index}`}>Start Time</Label>
                    <select
                      id={`common-start-${index}`}
                      value={slot.start}
                      onChange={(e) =>
                        updateCommonTimeSlot(
                          index,
                          "start",
                          Number.parseInt(e.target.value)
                        )
                      }
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    >
                      {TIME_OFFSETS.slice(0, -1).map((offset) => (
                        <option key={`${index}:${offset}`} value={offset}>
                          {formatOffsetToTime(offset)}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor={`common-end-${index}`}>End Time</Label>
                    <select
                      id={`common-end-${index}`}
                      value={slot.end}
                      onChange={(e) =>
                        updateCommonTimeSlot(
                          index,
                          "end",
                          Number.parseInt(e.target.value)
                        )
                      }
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    >
                      {TIME_OFFSETS.slice(1).map((offset) => (
                        <option key={offset} value={offset}>
                          {formatOffsetToTime(offset)}
                        </option>
                      ))}
                    </select>
                  </div>
                  <Button
                    type="button"
                    variant="destructive"
                    size="icon"
                    onClick={() => removeCommonTimeSlot(index)}
                    className="mt-6"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={addCommonTimeSlot}
              className="mt-4"
            >
              <Plus className="h-4 w-4 mr-2" /> Add Common Time Slot
            </Button>
          </CardContent>
        </Card>

        <Tabs
          defaultValue="existing"
          className="mb-6"
          onValueChange={setActiveTab}
        >
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="existing">Current Timeslots</TabsTrigger>
            <TabsTrigger value="new">New Timeslots</TabsTrigger>
          </TabsList>

          {/* Existing Timeslots Tab */}
          <TabsContent value="existing">
            <div className="space-y-6 mt-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Current Timeslots</h2>
                <div className="text-sm text-muted-foreground">
                  {existingSchedule.reduce(
                    (total, date) => total + date.timeSlots.length,
                    0
                  )}{" "}
                  timeslots
                </div>
              </div>

              {sortedExistingSchedule.length === 0 ? (
                <div className="flex flex-col items-center justify-center p-8 text-center border rounded-lg bg-muted/20">
                  <Clock className="h-10 w-10 text-muted-foreground mb-2" />
                  <p className="text-muted-foreground">
                    No current timeslots found
                  </p>
                </div>
              ) : (
                sortedExistingSchedule.map((item) => (
                  <Card key={item.date}>
                    <CardHeader>
                      <CardTitle>
                        {item.date
                          ? format(
                              fromUnixTime(item.date),
                              "EEEE, MMMM d, yyyy"
                            )
                          : "Unknown Date"}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {item.timeSlots.map((slot, index) => (
                          <div
                            key={index}
                            className="flex items-center justify-between p-3 border rounded-md"
                          >
                            <div className="flex items-center">
                              <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                              <span>
                                {formatUnixToTime(slot.start)} -{" "}
                                {formatUnixToTime(slot.end)}
                              </span>
                            </div>
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() =>
                                removeExistingTimeSlot(item.date, index)
                              }
                              className="text-destructive hover:text-destructive hover:bg-destructive/10"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </TabsContent>

          {/* New Timeslots Tab */}
          <TabsContent value="new">
            <div className="space-y-6 mt-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">New Timeslots</h2>
                <div className="text-sm text-muted-foreground">
                  {newSchedule.reduce(
                    (total, date) => total + date.timeSlots.length,
                    0
                  )}{" "}
                  timeslots
                </div>
              </div>

              <div className="mb-6">
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className="w-full justify-start text-left font-normal"
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {dateRange?.from ? (
                        dateRange.to ? (
                          <>
                            {format(dateRange.from, "LLL dd, y")} -{" "}
                            {format(dateRange.to, "LLL dd, y")}
                          </>
                        ) : (
                          format(dateRange.from, "LLL dd, y")
                        )
                      ) : (
                        <span>Pick date or drag to select range</span>
                      )}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      initialFocus
                      mode="range"
                      defaultMonth={dateRange?.from}
                      selected={dateRange}
                      onSelect={setDateRange}
                      numberOfMonths={2}
                    />
                  </PopoverContent>
                </Popover>
                <Button
                  type="button"
                  onClick={addDateRange}
                  className="mt-2 w-full"
                  disabled={!dateRange?.from}
                >
                  Add Selected Date(s) to Schedule
                </Button>
              </div>

              {sortedNewSchedule.length === 0 ? (
                <div className="flex flex-col items-center justify-center p-8 text-center border rounded-lg bg-muted/20">
                  <CalendarIcon className="h-10 w-10 text-muted-foreground mb-2" />
                  <p className="text-muted-foreground">
                    No new timeslots added yet
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Select dates from the calendar to add timeslots
                  </p>
                </div>
              ) : (
                <>
                  {newSchedule.length > 0 && (
                    <Button
                      type="button"
                      onClick={applyCommonTimeSlotsToAll}
                      className="w-full mb-4"
                    >
                      Apply Common Time Slots to All Dates
                    </Button>
                  )}

                  {sortedNewSchedule.map((item) => (
                    <Card key={item.date}>
                      <CardHeader>
                        <CardTitle className="flex justify-between items-center">
                          <span>
                            {item.date
                              ? format(
                                  fromUnixTime(item.date),
                                  "EEEE, MMMM d, yyyy"
                                )
                              : "Unknown Date"}
                          </span>
                          <div>
                            <Button
                              type="button"
                              variant="outline"
                              size="sm"
                              onClick={() =>
                                applyCommonTimeSlotsToDate(item.date)
                              }
                              className="mr-2"
                            >
                              <Copy className="h-4 w-4 mr-2" /> Apply Common
                              Slots
                            </Button>
                            <Button
                              type="button"
                              variant="destructive"
                              size="sm"
                              onClick={() => removeDate(item.date)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {item.timeSlots.map((slot, index) => (
                            <div
                              key={index}
                              className="flex items-center space-x-4"
                            >
                              <div className="grid gap-2">
                                <Label htmlFor={`${item.date}-start-${index}`}>
                                  Start Time
                                </Label>
                                <select
                                  id={`${item.date}-start-${index}`}
                                  value={getTimeOffsetFromUnix(slot.start)}
                                  onChange={(e) =>
                                    updateTimeSlot(
                                      item.date,
                                      index,
                                      "start",
                                      Number.parseInt(e.target.value)
                                    )
                                  }
                                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                                >
                                  {TIME_OFFSETS.slice(0, -1).map((offset) => (
                                    <option key={offset} value={offset}>
                                      {formatOffsetToTime(offset)}
                                    </option>
                                  ))}
                                </select>
                              </div>
                              <div className="grid gap-2">
                                <Label htmlFor={`${item.date}-end-${index}`}>
                                  End Time
                                </Label>
                                <select
                                  id={`${item.date}-end-${index}`}
                                  value={getTimeOffsetFromUnix(slot.end)}
                                  onChange={(e) =>
                                    updateTimeSlot(
                                      item.date,
                                      index,
                                      "end",
                                      Number.parseInt(e.target.value)
                                    )
                                  }
                                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                                >
                                  {TIME_OFFSETS.slice(1).map((offset) => (
                                    <option key={offset} value={offset}>
                                      {formatOffsetToTime(offset)}
                                    </option>
                                  ))}
                                </select>
                              </div>
                              <Button
                                type="button"
                                variant="destructive"
                                size="icon"
                                onClick={() => removeTimeSlot(item.date, index)}
                                className="mt-6"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          ))}
                          {item.timeSlots.map((slot, index) => {
                            const otherSlots = item.timeSlots.filter(
                              (_, i) => i !== index
                            );

                            return (
                              !isValidTimeSlot(
                                otherSlots,
                                slot.start,
                                slot.end
                              ) && (
                                <p
                                  key={`invalid-${index}`}
                                  className="text-sm text-red-500 mt-1"
                                >
                                  Invalid time slot. Ensure start time is before
                                  end time and time slots do not overlap.
                                </p>
                              )
                            );
                          })}
                        </div>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => addTimeSlot(item.date)}
                          className="mt-4"
                        >
                          <Plus className="h-4 w-4 mr-2" /> Add Time Slot
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </>
              )}
            </div>
          </TabsContent>
        </Tabs>

        <Separator className="my-6" />

        <div className="flex flex-col space-y-2">
          <div className="flex justify-between items-center mb-2">
            <div>
              <h3 className="text-lg font-medium">Schedule Summary</h3>
              <p className="text-sm text-muted-foreground">
                {existingSchedule.reduce(
                  (total, date) => total + date.timeSlots.length,
                  0
                )}{" "}
                current timeslots +
                {newSchedule.reduce(
                  (total, date) => total + date.timeSlots.length,
                  0
                )}{" "}
                new timeslots
              </p>
            </div>
          </div>
          <Button type="submit" size="lg">
            Save Schedule
          </Button>
        </div>
      </form>
    </div>
  );
}
