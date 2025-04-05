"use client";

import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Clock,
  MapPin,
  Search,
  Truck,
  Calendar,
  AlertCircle,
} from "lucide-react";
import { Input } from "@/components/ui/input";

// Update delivery status types to include cancellation states
type DeliveryStatus =
  | "Assigned To Driver"
  | "Picked up by Driver"
  | "Delivered by Driver"
  | "Received by Customer"
  | "Pending Cancellation"
  | "Cancelled"
  | "Escalated";

// Define delivery interface
interface Delivery {
  order_id: string;
  driver_id: string;
  timeslot: number; // Unix timestamp
  location: string;
  status: DeliveryStatus;
  delivery_id: number;
}

export default function DeliveryList() {
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  const [activeTab, setActiveTab] = useState<string>("all");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  // Fetch deliveries from API
  useEffect(() => {
    const fetchDeliveries = async () => {
      try {
        // Replace with your actual API endpoint
        const driver_id = localStorage.getItem("driver_id");
        const token = localStorage.getItem("auth_token");
        // Check if driver_id and token are available
        // If not, redirect to login page
        if (!driver_id || !token) {
          alert("Not authenticated. Please log in again.");
          window.location.href = "/login";
          return;
        }
        // Fetch deliveries from the API
        const response = await fetch(
          `http://localhost:5000/deliveries?driver_id=${driver_id}`
        );
        // add the portion below for JWT auth:
        // , {
        //   headers: {
        //     Authorization: `Bearer ${token}`,
        //   },
        // });

        console.log(response);
        const jsonResponse = await response.json();
        const data = jsonResponse.data;

        setDeliveries(data);
      } catch (error) {
        console.error("Error fetching deliveries:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDeliveries();
  }, []);

  // Format Unix timestamp to hour range and date
  const formatTimeslot = (
    unixTimestamp: number
  ): { timeRange: string; date: string } => {
    const date = new Date(unixTimestamp * 1000);

    // Format hours as 1800-1900
    const startHour = date.getHours();
    // const endHour = startHour + 1;

    // Pad with leading zeros and format as 1800-1900
    const startFormatted = startHour.toString().padStart(2, "0") + "00";
    const endFormatted = startHour.toString().padStart(2, "0") + "30";

    const timeRange = `${startFormatted}-${endFormatted}`;

    // Format date as DD/MM/YYYY
    const day = date.getDate().toString().padStart(2, "0");
    const month = (date.getMonth() + 1).toString().padStart(2, "0"); // Month is 0-indexed
    const year = date.getFullYear();

    const dateFormatted = `${day}/${month}/${year}`;

    return { timeRange, date: dateFormatted };
  };

  // Update delivery status
  const updateDeliveryStatus = async (
    delivery_id: number,
    newStatus: DeliveryStatus,
    order_id: string,
    timeslot: number,
    location: string
  ) => {
    try {
      // Update locally first for immediate UI feedback
      setDeliveries(
        deliveries.map((delivery) =>
          delivery.delivery_id === delivery_id
            ? { ...delivery, status: newStatus }
            : delivery
        )
      );

      // Send update to backend API
      await fetch(`http://localhost:5000/deliveries/${delivery_id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          order_id: order_id,
          status: newStatus,
          timeslot: timeslot,
          delivery_id: delivery_id,
          location: location,
        }),
      });
    } catch (error) {
      console.error("Error updating delivery status:", error);
      // Revert on error
      alert("Failed to update delivery status. Please try again.");
    }
  };

  // Request cancellation - only available for deliveries in "Assigned To Driver" status
  const requestCancellation = async (
    delivery_id: number,
    order_id: string,
    timeslot: number,
    location: string
  ) => {
    try {
      // Update status to "Pending Cancellation"
      await updateDeliveryStatus(
        delivery_id,
        "Pending Cancellation",
        order_id,
        timeslot,
        location
      );
    } catch (error) {
      console.error("Error requesting cancellation:", error);
      alert("Failed to request cancellation. Please try again.");
    }
  };

  // Get next status in the flow
  const getNextStatus = (
    currentStatus: DeliveryStatus
  ): DeliveryStatus | null => {
    switch (currentStatus) {
      case "Assigned To Driver":
        return "Picked up by Driver";
      case "Picked up by Driver":
        return "Delivered by Driver";
      case "Delivered by Driver":
        return "Received by Customer";
      default:
        return null;
    }
  };

  // Filter deliveries based on active tab and search term
  const filteredDeliveries = deliveries.filter((delivery) => {
    const { timeRange, date } = formatTimeslot(delivery.timeslot);
    const matchesTab = activeTab === "all" || delivery.status === activeTab;
    const matchesSearch =
      searchTerm === "" ||
      timeRange.includes(searchTerm) ||
      date.includes(searchTerm) ||
      delivery.location.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesTab && matchesSearch;
  });

  // Get status badge color and text
  const getStatusBadge = (status: DeliveryStatus) => {
    switch (status) {
      case "Assigned To Driver":
        return (
          <Badge
            variant="outline"
            className="bg-yellow-50 text-yellow-700 border-yellow-200"
          >
            Assigned
          </Badge>
        );
      case "Picked up by Driver":
        return (
          <Badge
            variant="outline"
            className="bg-blue-50 text-blue-700 border-blue-200"
          >
            Picked Up
          </Badge>
        );
      case "Delivered by Driver":
        return (
          <Badge
            variant="outline"
            className="bg-purple-50 text-purple-700 border-purple-200"
          >
            Delivered
          </Badge>
        );
      case "Received by Customer":
        return (
          <Badge
            variant="outline"
            className="bg-green-50 text-green-700 border-green-200"
          >
            Received
          </Badge>
        );
      case "Pending Cancellation":
        return (
          <Badge
            variant="outline"
            className="bg-orange-50 text-orange-700 border-orange-200"
          >
            Pending Cancel
          </Badge>
        );
      case "Cancelled":
        return (
          <Badge
            variant="outline"
            className="bg-red-50 text-red-700 border-red-200"
          >
            Cancelled
          </Badge>
        );
      case "Escalated":
        return (
          <Badge
            variant="outline"
            className="bg-rose-50 text-rose-700 border-rose-200"
          >
            Escalated
          </Badge>
        );
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-6 max-w-4xl flex justify-center items-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading deliveries...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-6 max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Driver Deliveries</h1>
        <div className="flex items-center gap-2">
          <Badge className="bg-primary">{deliveries.length} Total</Badge>
        </div>
      </div>

      <div className="mb-4 relative">
        <Input
          type="text"
          placeholder="Search deliveries..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10"
        />
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      </div>

      <Tabs defaultValue="all" className="w-full" onValueChange={setActiveTab}>
        <TabsList className="grid grid-cols-8 mb-4">
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="Assigned To Driver">Assigned</TabsTrigger>
          <TabsTrigger value="Picked up by Driver">Picked Up</TabsTrigger>
          <TabsTrigger value="Delivered by Driver">Delivered</TabsTrigger>
          <TabsTrigger value="Received by Customer">Received</TabsTrigger>
          <TabsTrigger value="Pending Cancellation">Pending Cancel</TabsTrigger>
          <TabsTrigger value="Cancelled">Cancelled</TabsTrigger>
          <TabsTrigger value="Escalated">Escalated</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="mt-0">
          <div className="grid gap-4">
            {filteredDeliveries.length > 0 ? (
              filteredDeliveries.map((delivery) => {
                const { timeRange, date } = formatTimeslot(delivery.timeslot);
                return (
                  <Card key={delivery.delivery_id} className="overflow-hidden">
                    <CardHeader className="pb-2">
                      <div className="flex justify-between items-start">
                        <CardTitle className="text-lg font-medium">
                          {delivery.delivery_id}
                        </CardTitle>
                        {getStatusBadge(delivery.status)}
                      </div>
                    </CardHeader>
                    <CardContent className="pb-3">
                      <div className="grid gap-3">
                        <div className="flex items-start gap-2">
                          <Calendar className="h-4 w-4 mt-1 text-muted-foreground" />
                          <span className="text-sm">{date}</span>
                        </div>
                        <div className="flex items-start gap-2">
                          <Clock className="h-4 w-4 mt-1 text-muted-foreground" />
                          <span className="text-sm">{timeRange}</span>
                        </div>
                        <div className="flex items-start gap-2">
                          <MapPin className="h-4 w-4 mt-1 text-muted-foreground" />
                          <span className="text-sm text-muted-foreground">
                            {delivery.location}
                          </span>
                        </div>
                        {delivery.status === "Pending Cancellation" && (
                          <div className="flex items-start gap-2">
                            <AlertCircle className="h-4 w-4 mt-1 text-orange-500" />
                            <span className="text-sm text-orange-500">
                              Cancellation requested - awaiting approval
                            </span>
                          </div>
                        )}
                        {delivery.status === "Cancelled" && (
                          <div className="flex items-start gap-2">
                            <AlertCircle className="h-4 w-4 mt-1 text-red-500" />
                            <span className="text-sm text-red-500">
                              This delivery has been cancelled
                            </span>
                          </div>
                        )}
                        {delivery.status === "Escalated" && (
                          <div className="flex items-start gap-2">
                            <AlertCircle className="h-4 w-4 mt-1 text-rose-500" />
                            <span className="text-sm text-rose-500">
                              This delivery has been escalated for review
                            </span>
                          </div>
                        )}
                      </div>
                    </CardContent>
                    <CardFooter className="flex flex-wrap gap-2 pt-0">
                      {/* Show regular status update button if not cancelled or pending cancellation */}
                      {getNextStatus(delivery.status) &&
                        delivery.status !== "Pending Cancellation" &&
                        delivery.status !== "Cancelled" && (
                          <Button
                            size="sm"
                            className="bg-primary hover:bg-primary/90"
                            onClick={() =>
                              updateDeliveryStatus(
                                delivery.delivery_id,
                                getNextStatus(delivery.status)!,
                                delivery.order_id,
                                delivery.timeslot,
                                delivery.location
                              )
                            }
                          >
                            <Truck className="mr-1 h-4 w-4" />
                            {delivery.status === "Assigned To Driver" &&
                              "Pick Up"}
                            {delivery.status === "Picked up by Driver" &&
                              "Mark Delivered"}
                            {delivery.status === "Delivered by Driver" &&
                              "Confirm Receipt"}
                          </Button>
                        )}

                      {/* Show cancellation request button only for assigned deliveries */}
                      {delivery.status === "Assigned To Driver" && (
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-red-200 text-red-700 hover:bg-red-50"
                          onClick={() =>
                            requestCancellation(
                              delivery.delivery_id,
                              delivery.order_id,
                              delivery.timeslot
                            )
                          }
                        >
                          <AlertCircle className="mr-1 h-4 w-4" />
                          Request Cancellation
                        </Button>
                      )}
                    </CardFooter>
                  </Card>
                );
              })
            ) : (
              <div className="text-center py-10 border rounded-lg bg-muted/20">
                <p className="text-muted-foreground">
                  No deliveries found matching your search or filter
                </p>
              </div>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
