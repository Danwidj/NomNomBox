"use client";

import type React from "react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Calendar } from "@/components/ui/calendar";
import { Plus, Trash2, CalendarIcon } from "lucide-react";
import { format, isSameDay, eachDayOfInterval } from "date-fns";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import type { DateRange } from "react-day-picker";

type TimeSlot = {
  start: string;
  end: string;
};

type DateSchedule = {
  date: Date;
  timeSlots: TimeSlot[];
};

const timeOptions = Array.from({ length: 29 }, (_, i) => {
  const hour = Math.floor(i / 2) + 8;
  const minute = i % 2 === 0 ? "00" : "30";
  return `${hour.toString().padStart(2, "0")}:${minute}`;
});

export default function DateBasedDriverSchedule() {
  const [schedule, setSchedule] = useState<DateSchedule[]>([]);
  const [dateRange, setDateRange] = useState<DateRange | undefined>();

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
            timeSlots: [{ start: "08:00", end: "09:00" }],
          })),
        ]);
        setDateRange(undefined);
        toast({
          title: "Dates added",
          description: `Added ${newDates.length} new date(s) to your schedule.`,
        });
      } else {
        toast({
          title: "No new dates added",
          description: "All selected dates are already in your schedule.",
          variant: "destructive",
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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically send the schedule to your backend API
    console.log("Submitted schedule:", schedule);
    toast({
      title: "Schedule Updated",
      description:
        "Your flexible working schedule has been successfully updated.",
    });
  };

  const isValidTimeSlot = (start: string, end: string) => {
    return start < end && start >= "08:00" && end <= "22:00";
  };

  // Sort schedule by date
  const sortedSchedule = [...schedule].sort(
    (a, b) => a.date.getTime() - b.date.getTime()
  );

  return (
    <div className="container mx-auto px-4 py-6 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">
        Set Your Flexible Working Schedule
      </h1>
      <form onSubmit={handleSubmit}>
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
                  <Button
                    type="button"
                    variant="destructive"
                    size="sm"
                    onClick={() => removeDate(item.date)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
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
                          {timeOptions.map((time) => (
                            <option key={time} value={time}>
                              {time}
                            </option>
                          ))}
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
                      !isValidTimeSlot(slot.start, slot.end) && (
                        <p
                          key={`invalid-${index}`}
                          className="text-sm text-red-500 mt-1"
                        >
                          Invalid time slot. Ensure start time is before end
                          time and within 8am to 10pm.
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
        <Button type="submit" className="mt-6 w-full">
          Save Schedule
        </Button>
      </form>
    </div>
  );
}
