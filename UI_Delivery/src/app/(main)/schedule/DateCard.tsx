import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Plus,
  Trash2,
  Copy,
  Clock,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { format, fromUnixTime } from "date-fns";
import { formatUnixToTime } from "./HelperFunctions";
import { useState } from "react";
import TimeSlotSelector from "./TimeSlotSelector";
type TimeSlot = {
  start: number;
  end: number;
  isExisting?: boolean;
  id?: number;
};
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertTriangle } from "lucide-react";
import { hasOverlappingTimeslot } from "./HelperFunctions";

export default function DateCard({
  date,
  timeSlots,
  onRemoveTimeSlot,
  onAddTimeSlot,
  onRemoveDate,
  onApplyCommonSlots,
  onUpdateTimeSlot,
  isExisting = false,
}: {
  date: number;
  timeSlots: TimeSlot[];
  onRemoveTimeSlot: (date: number, index: number) => void;
  onAddTimeSlot?: (date: number) => void;
  onRemoveDate?: (date: number) => void;
  onApplyCommonSlots?: (date: number) => void;
  onUpdateTimeSlot?: (
    date: number,
    index: number,
    field: "start" | "end",
    value: number
  ) => void;
  isExisting?: boolean;
}) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleOpen = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsOpen(!isOpen);
  };

  // Check for any overlapping timeslots
  const hasOverlaps = timeSlots.some(
    (slot, index) => hasOverlappingTimeslot(slot, timeSlots, index).overlaps
  );

  // Check for any invalid time ranges
  const hasInvalidRanges = timeSlots.some((slot) => slot.end <= slot.start);

  return (
    <Card key={date}>
      <CardHeader className="pb-2">
        <CardTitle className="flex justify-between items-center">
          <div className="flex items-center">
            <span>{format(fromUnixTime(date), "EEEE, MMMM d, yyyy")}</span>
            {(hasOverlaps || hasInvalidRanges) && !isExisting && (
              <div className="ml-2 text-destructive">
                <AlertTriangle className="h-4 w-4" />
              </div>
            )}
          </div>
          {!isExisting && (
            <div>
              {onApplyCommonSlots && (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => onApplyCommonSlots(date)}
                  className="mr-2"
                >
                  <Copy className="h-4 w-4 mr-2" /> Apply Common Slots
                </Button>
              )}
              {onRemoveDate && (
                <Button
                  type="button"
                  variant="destructive"
                  size="sm"
                  onClick={() => onRemoveDate(date)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
            </div>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="w-full">
          {/* Custom collapsible header */}
          <div
            onClick={toggleOpen}
            className="flex justify-between items-center p-2 mb-2 cursor-pointer hover:bg-muted/50 rounded-md"
          >
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-2" />
              <span>{timeSlots.length} timeslots</span>
            </div>
            {isOpen ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </div>

          {/* Collapsible content */}
          {isOpen && (
            <div className="space-y-2 mt-2">
              {isExisting ? (
                // Existing timeslots display
                timeSlots.map((slot, index) => (
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
                      onClick={(e) => {
                        e.stopPropagation();
                        onRemoveTimeSlot(date, index);
                      }}
                      className="text-destructive hover:text-destructive hover:bg-destructive/10"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))
              ) : (
                // New timeslots display with editors
                <div className="space-y-4">
                  {timeSlots.map((slot, index) => (
                    <TimeSlotSelector
                      key={index}
                      slot={slot}
                      date={date}
                      index={index}
                      updateTimeSlot={onUpdateTimeSlot}
                      removeTimeSlot={onRemoveTimeSlot}
                      allTimeSlots={timeSlots}
                    />
                  ))}
                </div>
              )}

              {/* Add time slot button for new timeslots */}
              {!isExisting && onAddTimeSlot && (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onAddTimeSlot(date);
                  }}
                  className="mt-4 w-full"
                >
                  <Plus className="h-4 w-4 mr-2" /> Add Time Slot
                </Button>
              )}

              {/* Warning for overlapping timeslots */}
              {hasOverlaps && !isExisting && (
                <Alert variant="destructive" className="mt-2">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle>Overlapping Timeslots</AlertTitle>
                  <AlertDescription>
                    Some timeslots overlap with each other. Please adjust them
                    before saving.
                  </AlertDescription>
                </Alert>
              )}

              {/* Warning for invalid time ranges */}
              {hasInvalidRanges && !isExisting && (
                <Alert variant="destructive" className="mt-2">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle>Invalid Time Ranges</AlertTitle>
                  <AlertDescription>
                    Some timeslots have end times before or equal to start
                    times. Please adjust them before saving.
                  </AlertDescription>
                </Alert>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
