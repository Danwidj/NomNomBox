"use client";

import type React from "react";

import { useEffect, useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Calendar } from "@/components/ui/calendar";
import { Plus, Trash2, CalendarIcon, Clock } from "lucide-react";
import {
  format,
  fromUnixTime,
  getUnixTime,
  startOfDay,
  addDays,
  isBefore,
} from "date-fns";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import type { DateRange } from "react-day-picker";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { formatOffsetToTime } from "./HelperFunctions";
import DateCard from "./DateCard";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertTriangle } from "lucide-react";
import { hasOverlappingTimeslot, doTimeslotsOverlap } from "./HelperFunctions";
import type { DateSchedule, TimeSlot } from "./HelperFunctions";
import axios from "axios";

// Time options from 08:00 to 22:00 in one-hour increments (in seconds)
const TIME_OFFSETS = Array.from({ length: 15 }, (_, i) => (i + 8) * 3600);

// Main component
export default function DateBasedDriverSchedule() {
  const [existingSchedule, setExistingSchedule] = useState<DateSchedule[]>([]);
  const [newSchedule, setNewSchedule] = useState<DateSchedule[]>([]);
  const [dateRange, setDateRange] = useState<DateRange | undefined>();
  const [activeTab, setActiveTab] = useState<string>("existing");
  const [commonTimeSlots, setCommonTimeSlots] = useState<TimeSlot[]>([
    { start: 8 * 3600, end: 12 * 3600 },
    { start: 13 * 3600, end: 17 * 3600 },
  ]);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  // Refs for tracking timeslots
  const originalTimeslots = useRef<number[]>([]);
  const deletedTimeslots = useRef<Set<number>>(new Set());
  //   const timeSlotsBeforeModification = useRef<Set<number>>(new Set());

  // Calculate tomorrow's date for calendar min date
  const tomorrow = addDays(new Date(), 1);

  // Load initial data
  useEffect(() => {
    const driver_id = localStorage.getItem("driver_id") || "1";

    // Mock data instead of making an API call with undefined URL
    // const mockTimeslots = [
    //   Math.floor(Date.now() / 1000), // Current time in Unix
    //   Math.floor(Date.now() / 1000) + 3600, // 1 hour later
    //   Math.floor(Date.now() / 1000) + 86400, // Tomorrow same time
    //   Math.floor(Date.now() / 1000) + 86400 + 3600, // Tomorrow 1 hour later
    // ];

    // Store original timeslots for tracking deletions
    // originalTimeslots.current = [...mockTimeslots];

    // const convertedSchedule = groupTimeSlotsByDate(mockTimeslots, true);
    // setExistingSchedule(convertedSchedule);

    // If you need to make an actual API call, uncomment and provide a valid URL:

    axios
      .get(
        `https://personal-6fbyxkeb.outsystemscloud.com/Driver/rest/DriverAPI/drivers/${driver_id}/timeslots`
      )
      .then((response) => {
        console.log("Fetched data:", response.data);
        if (Object.keys(response.data).length === 0) {
          setExistingSchedule([]);
          return;
        }
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
      const endTime = startTime + 3600;
      const dateTimestamp = getUnixTime(startOfDay(fromUnixTime(startTime)));

      if (!groupedByDate[dateTimestamp]) {
        groupedByDate[dateTimestamp] = [];
      }

      groupedByDate[dateTimestamp].push({
        start: startTime,
        end: endTime,
        isExisting,
        id: startTime,
      });
    });

    return Object.entries(groupedByDate).map(([dateStr, slots]) => ({
      date: Number(dateStr),
      timeSlots: slots,
    }));
  };

  // Helper to convert day offset seconds to Unix timestamp
  const offsetToUnixTime = (dateUnix: number, offsetSeconds: number) =>
    dateUnix + offsetSeconds;

  // Date range selection handlers
  const addDateRange = () => {
    if (!dateRange?.from) return;

    const fromUnix = getUnixTime(startOfDay(dateRange.from));
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
        ...newDays.map((day) => ({ date: day, timeSlots: [] })),
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
  };

  // Time slot handlers
  const removeExistingTimeSlot = (date: number, index: number) => {
    setExistingSchedule((prev) => {
      const timeslot = prev.find((item) => item.date === date)?.timeSlots[
        index
      ];

      if (timeslot?.id && originalTimeslots.current.includes(timeslot.id)) {
        deletedTimeslots.current.add(timeslot.id);
      }

      return prev
        .map((item) =>
          item.date === date
            ? {
                ...item,
                timeSlots: item.timeSlots.filter((_, i) => i !== index),
              }
            : item
        )
        .filter((item) => item.timeSlots.length > 0);
    });
  };

  const addTimeSlot = (date: number) => {
    setNewSchedule((prev) => {
      const dateSchedule = prev.find((item) => item.date === date);
      if (!dateSchedule) return prev;

      // Default new timeslot
      const newSlot = {
        start: offsetToUnixTime(date, 8 * 3600),
        end: offsetToUnixTime(date, 9 * 3600),
      };

      // Find a non-overlapping time if possible
      for (let hour = 8; hour < 21; hour++) {
        const testSlot = {
          start: offsetToUnixTime(date, hour * 3600),
          end: offsetToUnixTime(date, (hour + 1) * 3600),
        };

        if (
          !hasOverlappingTimeslot(testSlot, dateSchedule.timeSlots).overlaps
        ) {
          return prev.map((item) =>
            item.date === date
              ? { ...item, timeSlots: [...item.timeSlots, testSlot] }
              : item
          );
        }
      }

      // If all slots are taken, add the default one anyway
      return prev.map((item) =>
        item.date === date
          ? { ...item, timeSlots: [...item.timeSlots, newSlot] }
          : item
      );
    });
  };

  const removeTimeSlot = (date: number, index: number) => {
    setNewSchedule((prev) =>
      prev
        .map((item) =>
          item.date === date
            ? {
                ...item,
                timeSlots: item.timeSlots.filter((_, i) => i !== index),
              }
            : item
        )
        .filter((item) => item.timeSlots.length > 0)
    );

    // Clear validation errors when removing a timeslot
    validateSchedule();
  };

  // Update the updateTimeSlot function to check for overlaps
  const updateTimeSlot = (
    date: number,
    index: number,
    field: "start" | "end",
    offsetSeconds: number
  ) => {
    setNewSchedule((prev) => {
      const updatedSchedule = prev.map((item) => {
        if (item.date === date) {
          const updatedTimeSlots = item.timeSlots.map((slot, i) => {
            if (i === index) {
              const updatedSlot = {
                ...slot,
                [field]: offsetToUnixTime(date, offsetSeconds),
              };

              // Check for overlaps
              const { overlaps } = hasOverlappingTimeslot(
                updatedSlot,
                item.timeSlots,
                index
              );
              if (overlaps) {
                toast.warning("Overlapping timeslot", {
                  description: "This timeslot overlaps with another timeslot.",
                });
              }

              // Check for invalid time range
              if (field === "end" && updatedSlot.end <= updatedSlot.start) {
                toast.warning("Invalid time range", {
                  description: "End time must be after start time.",
                });
              }

              return updatedSlot;
            }
            return slot;
          });

          return { ...item, timeSlots: updatedTimeSlots };
        }
        return item;
      });

      // Validate the updated schedule
      validateSchedule(updatedSchedule);

      return updatedSchedule;
    });
  };

  const removeDate = (date: number) => {
    setNewSchedule((prev) => {
      const updatedSchedule = prev.filter((item) => item.date !== date);
      validateSchedule(updatedSchedule);
      return updatedSchedule;
    });
  };

  // Common time slots handlers
  const addCommonTimeSlot = () => {
    setCommonTimeSlots((prev) => [...prev, { start: 8 * 3600, end: 9 * 3600 }]);
  };

  const removeCommonTimeSlot = (index: number) => {
    setCommonTimeSlots((prev) => prev.filter((_, i) => i !== index));
  };

  const updateCommonTimeSlot = (
    index: number,
    field: "start" | "end",
    offsetSeconds: number
  ) => {
    setCommonTimeSlots((prev) => {
      const updated = prev.map((slot, i) => {
        if (i === index) {
          const updatedSlot = { ...slot, [field]: offsetSeconds };

          // Check for invalid time range
          if (field === "end" && updatedSlot.end <= updatedSlot.start) {
            toast.warning("Invalid time range", {
              description: "End time must be after start time.",
            });
          }

          return updatedSlot;
        }
        return slot;
      });

      // Check for overlaps in common time slots
      for (let i = 0; i < updated.length; i++) {
        for (let j = i + 1; j < updated.length; j++) {
          if (doTimeslotsOverlap(updated[i], updated[j])) {
            toast.warning("Overlapping common time slots", {
              description: "Some common time slots overlap with each other.",
            });
            break;
          }
        }
      }

      return updated;
    });
  };

  // Update the applyCommonTimeSlotsToDate function to ensure proper validation
  const applyCommonTimeSlotsToDate = (date: number) => {
    // Validate common time slots
    let hasInvalidTimeRanges = false;
    let hasOverlappingSlots = false;

    // Check for invalid time ranges
    commonTimeSlots.forEach((slot) => {
      if (slot.end <= slot.start) {
        hasInvalidTimeRanges = true;
      }
    });

    // Check for overlaps in common time slots
    for (let i = 0; i < commonTimeSlots.length; i++) {
      for (let j = i + 1; j < commonTimeSlots.length; j++) {
        if (doTimeslotsOverlap(commonTimeSlots[i], commonTimeSlots[j])) {
          hasOverlappingSlots = true;
          break;
        }
      }
      if (hasOverlappingSlots) break;
    }

    if (hasInvalidTimeRanges) {
      toast.error("Invalid common time slot", {
        description: "End time must be after start time in common time slots.",
      });
      return;
    }

    if (hasOverlappingSlots) {
      toast.error("Overlapping common time slots", {
        description: "Some common time slots overlap with each other.",
      });
      return;
    }

    setNewSchedule((prev) => {
      const updatedSchedule = prev.map((item) => {
        if (item.date === date) {
          // Create individual hour slots
          const individualSlots: TimeSlot[] = [];

          commonTimeSlots.forEach((commonSlot) => {
            const startHour = Math.floor(commonSlot.start / 3600);
            const endHour = Math.floor(commonSlot.end / 3600);

            for (let hour = startHour; hour < endHour; hour++) {
              const newSlot = {
                start: offsetToUnixTime(date, hour * 3600),
                end: offsetToUnixTime(date, (hour + 1) * 3600),
              };

              // Only add if it doesn't overlap with existing slots
              if (
                !individualSlots.some((slot) =>
                  doTimeslotsOverlap(slot, newSlot)
                )
              ) {
                individualSlots.push(newSlot);
              }
            }
          });

          return {
            ...item,
            timeSlots: individualSlots,
          };
        }
        return item;
      });

      validateSchedule(updatedSchedule);
      return updatedSchedule;
    });

    toast.success("Common Time Slots Applied");
  };

  // Update the applyCommonTimeSlotsToAll function to ensure proper validation
  const applyCommonTimeSlotsToAll = () => {
    // Validate common time slots
    let hasInvalidTimeRanges = false;
    let hasOverlappingSlots = false;

    // Check for invalid time ranges
    commonTimeSlots.forEach((slot) => {
      if (slot.end <= slot.start) {
        hasInvalidTimeRanges = true;
      }
    });

    // Check for overlaps in common time slots
    for (let i = 0; i < commonTimeSlots.length; i++) {
      for (let j = i + 1; j < commonTimeSlots.length; j++) {
        if (doTimeslotsOverlap(commonTimeSlots[i], commonTimeSlots[j])) {
          hasOverlappingSlots = true;
          break;
        }
      }
      if (hasOverlappingSlots) break;
    }

    if (hasInvalidTimeRanges) {
      toast.error("Invalid common time slot", {
        description: "End time must be after start time in common time slots.",
      });
      return;
    }

    if (hasOverlappingSlots) {
      toast.error("Overlapping common time slots", {
        description: "Some common time slots overlap with each other.",
      });
      return;
    }

    setNewSchedule((prev) => {
      const updatedSchedule = prev.map((item) => {
        // Create individual hour slots
        const individualSlots: TimeSlot[] = [];

        commonTimeSlots.forEach((commonSlot) => {
          const startHour = Math.floor(commonSlot.start / 3600);
          const endHour = Math.floor(commonSlot.end / 3600);

          for (let hour = startHour; hour < endHour; hour++) {
            const newSlot = {
              start: offsetToUnixTime(item.date, hour * 3600),
              end: offsetToUnixTime(item.date, (hour + 1) * 3600),
            };

            // Only add if it doesn't overlap with existing slots
            if (
              !individualSlots.some((slot) => doTimeslotsOverlap(slot, newSlot))
            ) {
              individualSlots.push(newSlot);
            }
          }
        });

        return {
          ...item,
          timeSlots: individualSlots,
        };
      });

      validateSchedule(updatedSchedule);
      return updatedSchedule;
    });

    toast.success("Common Time Slots Applied to All Dates");
  };

  // Calendar date disabler function - disable dates before tomorrow
  const disableDates = (date: Date) => {
    return isBefore(date, tomorrow);
  };

  // Validate the entire schedule for errors
  const validateSchedule = (scheduleToValidate = newSchedule) => {
    const errors: string[] = [];

    // Check for empty days
    const emptyDays = scheduleToValidate.filter(
      (day) => day.timeSlots.length === 0
    );
    if (emptyDays.length > 0) {
      errors.push("Some days have no timeslots");
    }

    // Check for invalid time ranges and overlaps
    scheduleToValidate.forEach((day) => {
      // Check for invalid time ranges
      day.timeSlots.forEach((slot) => {
        if (slot.end <= slot.start) {
          errors.push(
            `Invalid time range on ${format(
              fromUnixTime(day.date),
              "MMMM d, yyyy"
            )}`
          );
        }
      });

      // Check for overlapping timeslots within new schedule
      for (let i = 0; i < day.timeSlots.length; i++) {
        for (let j = i + 1; j < day.timeSlots.length; j++) {
          if (doTimeslotsOverlap(day.timeSlots[i], day.timeSlots[j])) {
            errors.push(
              `Overlapping timeslots on ${format(
                fromUnixTime(day.date),
                "MMMM d, yyyy"
              )}`
            );
            break;
          }
        }
      }

      // Check for overlaps with existing schedule
      const existingDay = existingSchedule.find(
        (item) => item.date === day.date
      );
      if (existingDay) {
        for (const newSlot of day.timeSlots) {
          for (const existingSlot of existingDay.timeSlots) {
            // Skip slots that are marked for deletion
            if (
              existingSlot.id &&
              deletedTimeslots.current.has(existingSlot.id)
            ) {
              continue;
            }

            if (doTimeslotsOverlap(newSlot, existingSlot)) {
              errors.push(
                `New timeslot overlaps with existing timeslot on ${format(
                  fromUnixTime(day.date),
                  "MMMM d, yyyy"
                )}`
              );
              break;
            }
          }
        }
      }
    });

    setValidationErrors(errors);
    return errors.length === 0;
  };

  // Update the handleSubmit function to break down timeslots into individual hours and add validations

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(newSchedule);

    if (!validateSchedule()) {
      toast.error("Please fix all validation errors before saving", {
        description: validationErrors.join(", "),
      });
      return;
    }

    // Additional check for overlaps between new and existing timeslots
    let hasOverlaps = false;
    for (const newDateSchedule of newSchedule) {
      const existingDateSchedule = existingSchedule.find(
        (item) => item.date === newDateSchedule.date
      );

      if (existingDateSchedule) {
        for (const newSlot of newDateSchedule.timeSlots) {
          for (const existingSlot of existingDateSchedule.timeSlots) {
            // Skip slots that are marked for deletion
            if (
              existingSlot.id &&
              deletedTimeslots.current.has(existingSlot.id)
            ) {
              continue;
            }

            if (doTimeslotsOverlap(newSlot, existingSlot)) {
              hasOverlaps = true;
              toast.error("Overlap detected", {
                description: `New timeslot overlaps with existing timeslot on ${format(
                  fromUnixTime(newDateSchedule.date),
                  "MMMM d, yyyy"
                )}`,
              });
              break;
            }
          }
          if (hasOverlaps) break;
        }
      }
      if (hasOverlaps) break;
    }

    if (hasOverlaps) {
      return;
    }

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

    // toast.success("Schedule Updated", {
    //   description:
    //     "Your flexible working schedule has been successfully updated.",
    // });

    // Switch to existing tab
    setActiveTab("existing");

    // In a real implementation, you would reset the changes array after a successful API call:
    const endpoint = "http://localhost:5011/availability";
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
        console.log("Error updating schedule:", error);
        toast.error(
          "Failed to update schedule. One of the timeslots you are attempting to delete already has an assigned delivery"
        );
        setTimeout(() => {
          window.location.reload();
        }, 1500);
        deletedTimeslots.current.clear();
      });
  };

  // Sort schedules by date
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
        {/* Common Time Slots */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Common Time Slots</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {commonTimeSlots.map((slot, index) => (
                <div key={index} className="flex items-center space-x-4">
                  <div className="grid gap-2">
                    <Label>Start Time</Label>
                    <select
                      value={slot.start}
                      onChange={(e) =>
                        updateCommonTimeSlot(
                          index,
                          "start",
                          Number(e.target.value)
                        )
                      }
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    >
                      {TIME_OFFSETS.slice(0, -1).map((offset) => (
                        <option key={offset} value={offset}>
                          {formatOffsetToTime(offset)}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="grid gap-2">
                    <Label>End Time</Label>
                    <select
                      value={slot.end}
                      onChange={(e) =>
                        updateCommonTimeSlot(
                          index,
                          "end",
                          Number(e.target.value)
                        )
                      }
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
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

        {/* Validation Errors */}
        {validationErrors.length > 0 && (
          <Alert variant="destructive" className="mb-6">
            <AlertTriangle className="h-4 w-4" />
            <AlertTitle>Validation Errors</AlertTitle>
            <AlertDescription>
              <ul className="list-disc pl-5 mt-2">
                {validationErrors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </AlertDescription>
          </Alert>
        )}

        {/* Tabs */}
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
                  timeslots across {existingSchedule.length} dates
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
                  <DateCard
                    key={item.date}
                    date={item.date}
                    timeSlots={item.timeSlots}
                    onRemoveTimeSlot={removeExistingTimeSlot}
                    isExisting={true}
                  />
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
                  timeslots across {newSchedule.length} dates
                </div>
              </div>

              {/* Date Selection */}
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
                      defaultMonth={tomorrow}
                      selected={dateRange}
                      onSelect={setDateRange}
                      numberOfMonths={2}
                      disabled={disableDates}
                      fromDate={tomorrow}
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
                    <DateCard
                      key={item.date}
                      date={item.date}
                      timeSlots={item.timeSlots}
                      onRemoveTimeSlot={removeTimeSlot}
                      onAddTimeSlot={addTimeSlot}
                      onRemoveDate={removeDate}
                      onApplyCommonSlots={applyCommonTimeSlotsToDate}
                      onUpdateTimeSlot={updateTimeSlot}
                    />
                  ))}
                </>
              )}
            </div>
          </TabsContent>
        </Tabs>

        <Separator className="my-6" />

        {/* Submit Button */}
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
          <Button
            type="submit"
            size="lg"
            disabled={
              newSchedule.length === 0 && deletedTimeslots.current.size === 0
            }
          >
            Save Schedule
          </Button>
          {validationErrors.length > 0 && (
            <p className="text-sm text-destructive text-center">
              Please fix all validation errors before saving
            </p>
          )}
        </div>
      </form>
    </div>
  );
}
