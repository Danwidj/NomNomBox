import { Button } from "@/components/ui/button";

import { Label } from "@/components/ui/label";

import { Trash2 } from "lucide-react";
import { fromUnixTime, getUnixTime, startOfDay } from "date-fns";
import { formatOffsetToTime } from "./HelperFunctions";
// import { formatUnixToTime } from "./HelperFunctions";
import { AlertTriangle } from "lucide-react";
import { hasOverlappingTimeslot } from "./HelperFunctions";

const TIME_OFFSETS = Array.from({ length: 15 }, (_, i) => (i + 8) * 3600);
type TimeSlot = {
  start: number;
  end: number;
  isExisting?: boolean;
  id?: number;
};

export default function TimeSlotSelector({
  slot,
  date,
  index,
  updateTimeSlot,
  removeTimeSlot,
  allTimeSlots,
}: {
  slot: TimeSlot;
  date: number;
  index: number;
  updateTimeSlot: (
    date: number,
    index: number,
    field: "start" | "end",
    value: number
  ) => void;
  removeTimeSlot: (date: number, index: number) => void;
  allTimeSlots: TimeSlot[];
}) {
  const getTimeOffsetFromUnix = (unix: number) => {
    const dayStart = getUnixTime(startOfDay(fromUnixTime(unix)));
    return unix - dayStart;
  };

  // Check for overlaps with other timeslots
  const { overlaps } = hasOverlappingTimeslot(slot, allTimeSlots, index);

  return (
    <div className="space-y-2">
      <div className="flex items-center space-x-4">
        <div className="grid gap-2">
          <Label htmlFor={`${date}-start-${index}`}>Start Time</Label>
          <select
            id={`${date}-start-${index}`}
            value={getTimeOffsetFromUnix(slot.start)}
            onChange={(e) =>
              updateTimeSlot(date, index, "start", Number(e.target.value))
            }
            className={`w-full rounded-md border ${
              overlaps ? "border-destructive" : "border-input"
            } bg-background px-3 py-2 text-sm`}
          >
            {TIME_OFFSETS.slice(0, -1).map((offset) => (
              <option key={offset} value={offset}>
                {formatOffsetToTime(offset)}
              </option>
            ))}
          </select>
        </div>
        <div className="grid gap-2">
          <Label htmlFor={`${date}-end-${index}`}>End Time</Label>
          <select
            id={`${date}-end-${index}`}
            value={getTimeOffsetFromUnix(slot.end)}
            onChange={(e) =>
              updateTimeSlot(date, index, "end", Number(e.target.value))
            }
            className={`w-full rounded-md border ${
              overlaps ? "border-destructive" : "border-input"
            } bg-background px-3 py-2 text-sm`}
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
          onClick={() => removeTimeSlot(date, index)}
          className="mt-6"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>

      {overlaps && (
        <div className="text-xs text-destructive flex items-center">
          <AlertTriangle className="h-3 w-3 mr-1" />
          This timeslot overlaps with another timeslot
        </div>
      )}

      {slot.end <= slot.start && (
        <div className="text-xs text-destructive flex items-center">
          <AlertTriangle className="h-3 w-3 mr-1" />
          End time must be after start time
        </div>
      )}
    </div>
  );
}
