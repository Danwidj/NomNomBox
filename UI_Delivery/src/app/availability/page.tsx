"use client";
import { Card, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { useEffect, useState } from "react";
import { DateRange } from "react-day-picker";

export default function AvailabilityCard() {
  const [dates, setDates] = useState<DateRange | undefined>(undefined);
  const [intermediateDates, setIntermediateDates] = useState<Date[] | []>([]);
  function getDatesInRange(startDate: Date, endDate: Date): Date[] {
    const date = new Date(startDate.getTime());

    const dates = [];

    while (date <= endDate) {
      dates.push(new Date(date));
      date.setDate(date.getDate() + 1);
    }

    return dates;
  }

  useEffect(() => {
    if (dates?.from && dates?.to) {
      const intermediateDateArr = getDatesInRange(dates.from, dates.to);
      setIntermediateDates(intermediateDateArr);
    }
  }, [dates]);

  const onSelectDate = (date: DateRange) => {
    setDates(date);
    console.log(date);
  };

  return (
    <>
      <div className="w-fit m-auto">
        <h1>Delivery Management</h1>
        <Calendar mode="range" selected={dates} onSelect={onSelectDate} />
        <Button>Create your schedule</Button>
        {intermediateDates.length == 0
          ? ""
          : intermediateDates.map((date) => (
              <Card key={date}>
                <CardTitle>
                  {date.toLocaleDateString("en-GB", {
                    day: "numeric",
                    month: "long",
                    year: "numeric",
                  })}
                </CardTitle>
              </Card>
            ))}
      </div>
    </>
  );
}
