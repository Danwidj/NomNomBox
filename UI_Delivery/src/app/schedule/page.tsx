"use client";

import type React from "react";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Calendar } from "@/components/ui/calendar";
import { Plus, Trash2, CalendarIcon, Copy } from "lucide-react";
import { format, isSameDay, eachDayOfInterval } from "date-fns";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import type { DateRange } from "react-day-picker";
import axios from "axios";

type TimeSlot = {
  start: string;
  end: string;
};

type DateSchedule = {
  date: Date;
  timeSlots: TimeSlot[];
};

const timeOptions = Array.from({ length: 15 }, (_, i) => {
  const hour = Math.floor(i) + 8;
  const minute = "00";
  return `${hour.toString().padStart(2, "0")}:${minute}`;
});

export default function DateBasedDriverSchedule() {
  const [schedule, setSchedule] = useState<DateSchedule[]>([]);
  const [dateRange, setDateRange] = useState<DateRange | undefined>();
  const [commonTimeSlots, setCommonTimeSlots] = useState<TimeSlot[]>([
    { start: "08:00", end: "12:00" },
    { start: "13:00", end: "17:00" },
  ]);

  //grab data first
  // useEffect(() => {
  //   axios.get("https://api.example.com/schedule").then((response) => {
  //     setSchedule(response.data);
  //   });
  // }, []);

  const addDateRange = () => {
    if (dateRange?.from && dateRange?.to) {
      const newDates = eachDayOfInterval({
        start: dateRange.from,
        end: dateRange.to,
      }).filter((date) => !schedule.some((item) => isSameDay(item.date, date)));

      if (newDates.length > 0) {
        setSchedule((prev) => [
          ...prev,
          ...newDates.map((date) => ({
            date,
            timeSlots: [],
          })),
        ]);
        setDateRange(undefined);
        toast.success("Dates added", {
          description: `Added ${newDates.length} new date(s) to your schedule.`,
        });
      } else {
        toast.info("No new dates added", {
          description: "All selected dates are already in your schedule.",
        });
      }
    }
  };

  const removeDate = (date: Date) => {
    setSchedule((prev) => prev.filter((item) => !isSameDay(item.date, date)));
  };

  const addTimeSlot = (date: Date) => {
    setSchedule((prev) =>
      prev.map((item) =>
        isSameDay(item.date, date)
          ? {
              ...item,
              timeSlots: [...item.timeSlots, { start: "08:00", end: "09:00" }],
            }
          : item
      )
    );
  };

  const removeTimeSlot = (date: Date, index: number) => {
    setSchedule((prev) =>
      prev.map((item) =>
        isSameDay(item.date, date)
          ? { ...item, timeSlots: item.timeSlots.filter((_, i) => i !== index) }
          : item
      )
    );
  };

  const updateTimeSlot = (
    date: Date,
    index: number,
    field: "start" | "end",
    value: string
  ) => {
    setSchedule((prev) =>
      prev.map((item) =>
        isSameDay(item.date, date)
          ? {
              ...item,
              timeSlots: item.timeSlots.map((slot, i) =>
                i === index ? { ...slot, [field]: value } : slot
              ),
            }
          : item
      )
    );
  };

  const addCommonTimeSlot = () => {
    setCommonTimeSlots((prev) => [...prev, { start: "08:00", end: "09:00" }]);
  };

  const removeCommonTimeSlot = (index: number) => {
    setCommonTimeSlots((prev) => prev.filter((_, i) => i !== index));
  };

  const updateCommonTimeSlot = (
    index: number,
    field: "start" | "end",
    value: string
  ) => {
    setCommonTimeSlots((prev) =>
      prev.map((slot, i) => (i === index ? { ...slot, [field]: value } : slot))
    );
  };

  const applyCommonTimeSlotsToAll = () => {
    for (let index = 0; index < commonTimeSlots.length; index++) {
      const item = commonTimeSlots[index];
      if (item.start > item.end) {
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

    setSchedule((prev) =>
      prev.map((item) => ({
        ...item,
        timeSlots: [...commonTimeSlots],
      }))
    );
    toast.success("Common Time Slots Applied", {
      description: "Applied common time slots to all dates in your schedule.",
    });
  };

  const applyCommonTimeSlotsToDate = (date: Date) => {
    setSchedule((prev) =>
      prev.map((item) =>
        isSameDay(item.date, date)
          ? { ...item, timeSlots: [...commonTimeSlots] }
          : item
      )
    );
    toast.success("Common Time Slots Applied", {
      description: `Applied common time slots to ${format(
        date,
        "MMMM d, yyyy"
      )}.`,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Send request to backend
    console.log("Submitted schedule:", schedule);
    type Schedule = {
      startTime: number;
      endTime: number;
    };
    type SubmittedData = {
      driverId: number;
      schedule: Schedule[];
    };
    // get driver id from local storage
    const submittedData: SubmittedData = { driverId: 1, schedule: [] };

    // Convert the `date` property to Unix timestamp (in seconds)
    for (const dateSchedule of schedule) {
      const dateUnix = Math.floor(new Date(dateSchedule.date).getTime() / 1000);

      // Convert the `start` and `end` times to Unix timestamps (using the `date` as base)
      const timeSlotsUnix = dateSchedule.timeSlots.map((slot) => {
        // Combine the date and start time to create a full date string
        const startDateTime = new Date(dateSchedule.date);
        const [startHours, startMinutes] = slot.start.split(":");
        startDateTime.setHours(
          parseInt(startHours),
          parseInt(startMinutes),
          0,
          0
        );

        // Combine the date and end time to create a full date string
        const endDateTime = new Date(dateSchedule.date);
        const [endHours, endMinutes] = slot.end.split(":");
        endDateTime.setHours(parseInt(endHours), parseInt(endMinutes), 0, 0);

        submittedData.schedule.push({
          startTime: Math.floor(startDateTime.getTime() / 1000), // Convert to Unix timestamp
          endTime: Math.floor(endDateTime.getTime() / 1000), // Convert to Unix timestamp
        });
      });
    }
    toast.success("Schedule Updated", {
      description:
        "Your flexible working schedule has been successfully updated.",
    });
    console.log("Submitted data:", submittedData);

    // axios.post(())
  };
  function convertTimeToDate(timeString: string) {
    const date = new Date();
    const [hours, minutes] = timeString.split(":").map(Number);
    date.setHours(hours, minutes, 0, 0); // Set the time, with zero seconds and milliseconds
    return date;
  }
  const isValidTimeSlot = (
    timeslots: TimeSlot[],
    start: string,
    end: string
  ) => {
    if (start > end) {
      return false;
    }
    if (timeslots.length === 0) {
      return true;
    }
    for (const timeslot of timeslots) {
      const startTime = convertTimeToDate(start);
      if (
        startTime >= convertTimeToDate(timeslot.start) &&
        startTime < convertTimeToDate(timeslot.end)
      ) {
        return false;
      }
    }
    return true;
  };

  // Sort schedule by date
  const sortedSchedule = [...schedule].sort(
    (a, b) => a.date.getTime() - b.date.getTime()
  );

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
                        updateCommonTimeSlot(index, "start", e.target.value)
                      }
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    >
                      {timeOptions.map(
                        (time) =>
                          time != "22:00" && (
                            <option key={`${index}:${time}`} value={time}>
                              {time}
                            </option>
                          )
                      )}
                    </select>
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor={`common-end-${index}`}>End Time</Label>
                    <select
                      id={`common-end-${index}`}
                      value={slot.end}
                      onChange={(e) =>
                        updateCommonTimeSlot(index, "end", e.target.value)
                      }
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    >
                      {timeOptions.map((time) => (
                        <option key={time} value={time}>
                          {time}
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
              {/* {for (const [index, slot] of commonTimeSlots.entries())
                !isValidTimeSlot(
              ) && ""} */}
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
            {schedule.length > 0 && (
              <Button
                type="button"
                onClick={applyCommonTimeSlotsToAll}
                className="mt-4 ml-4"
              >
                Apply to All Dates
              </Button>
            )}
          </CardContent>
        </Card>

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
        <div className="space-y-6">
          {sortedSchedule.map((item) => (
            <Card key={item.date.toISOString()}>
              <CardHeader>
                <CardTitle className="flex justify-between items-center">
                  <span>{format(item.date, "EEEE, MMMM d, yyyy")}</span>
                  <div>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => applyCommonTimeSlotsToDate(item.date)}
                      className="mr-2"
                    >
                      <Copy className="h-4 w-4 mr-2" /> Apply Common Slots
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
                    <div key={index} className="flex items-center space-x-4">
                      <div className="grid gap-2">
                        <Label
                          htmlFor={`${item.date.toISOString()}-start-${index}`}
                        >
                          Start Time
                        </Label>
                        <select
                          id={`${item.date.toISOString()}-start-${index}`}
                          value={slot.start}
                          onChange={(e) =>
                            updateTimeSlot(
                              item.date,
                              index,
                              "start",
                              e.target.value
                            )
                          }
                          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                        >
                          {timeOptions.map(
                            (time) =>
                              time != "22:00" && (
                                <option key={time} value={time}>
                                  {time}
                                </option>
                              )
                          )}
                        </select>
                      </div>
                      <div className="grid gap-2">
                        <Label
                          htmlFor={`${item.date.toISOString()}-end-${index}`}
                        >
                          End Time
                        </Label>
                        <select
                          id={`${item.date.toISOString()}-end-${index}`}
                          value={slot.end}
                          onChange={(e) =>
                            updateTimeSlot(
                              item.date,
                              index,
                              "end",
                              e.target.value
                            )
                          }
                          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                        >
                          {timeOptions.map((time) => (
                            <option key={time} value={time}>
                              {time}
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
                  {item.timeSlots.map(
                    (slot, index) =>
                      !isValidTimeSlot(
                        item.timeSlots.filter((_, i) => i !== index),
                        slot.start,
                        slot.end
                      ) && (
                        <p
                          key={`invalid-${index}`}
                          className="text-sm text-red-500 mt-1"
                        >
                          Invalid time slot. Ensure start time is before end
                          time and time slots do not overlap.
                        </p>
                      )
                  )}
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
        </div>
        <Button type="submit" className="mt-6 w-full" onClick={handleSubmit}>
          Save Schedule
        </Button>
      </form>
    </div>
  );
}
