import { format, fromUnixTime } from "date-fns";

// Types
export type TimeSlot = {
  start: number;
  end: number;
  isExisting?: boolean;
  id?: number;
};

export type DateSchedule = {
  date: number;
  timeSlots: TimeSlot[];
};

export const formatUnixToTime = (unix: number) => {
  try {
    return format(fromUnixTime(unix), "HH:mm");
  } catch (error) {
    return "00:00";
  }
};

export const formatOffsetToTime = (offsetSeconds: number) => {
  const hours = Math.floor(offsetSeconds / 3600);
  const minutes = Math.floor((offsetSeconds % 3600) / 60);
  return `${hours.toString().padStart(2, "0")}:${minutes
    .toString()
    .padStart(2, "0")}`;
};

export const doTimeslotsOverlap = (
  slot1: TimeSlot,
  slot2: TimeSlot
): boolean => {
  // Same timeslot
  if (slot1.start === slot2.start && slot1.end === slot2.end) {
    return true;
  }

  // Check for overlap
  return (
    (slot1.start < slot2.end && slot1.end > slot2.start) || // General overlap
    (slot1.start <= slot2.start && slot1.end >= slot2.end) || // slot1 contains slot2
    (slot2.start <= slot1.start && slot2.end >= slot1.end) // slot2 contains slot1
  );
};

export const hasOverlappingTimeslot = (
  slot: TimeSlot,
  existingSlots: TimeSlot[],
  excludeIndex = -1
): { overlaps: boolean; overlapIndex: number } => {
  for (let i = 0; i < existingSlots.length; i++) {
    if (i === excludeIndex) continue; // Skip the slot being edited

    if (doTimeslotsOverlap(slot, existingSlots[i])) {
      return { overlaps: true, overlapIndex: i };
    }
  }

  return { overlaps: false, overlapIndex: -1 };
};
