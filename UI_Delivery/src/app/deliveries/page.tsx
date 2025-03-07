"use client";

import { useState } from "react";
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
  CheckCircle,
  Clock,
  MapPin,
  Package,
  ThumbsDown,
  ThumbsUp,
  Truck,
  User,
  XCircle,
  Search,
} from "lucide-react";
import { Input } from "@/components/ui/input";

// Define delivery status types
type DeliveryStatus =
  | "pending"
  | "accepted"
  | "rejected"
  | "in_progress"
  | "passed"
  | "failed";

// Define delivery interface
interface Delivery {
  id: string;
  customerName: string;
  address: string;
  deliveryTime: string;
  items: string;
  status: DeliveryStatus;
  distance: string;
}

// Sample delivery data
const initialDeliveries: Delivery[] = [
  {
    id: "DEL-1001",
    customerName: "John Smith",
    address: "123 Main St, Anytown, CA 94123",
    deliveryTime: "10:00 AM - 12:00 PM",
    items: "2 packages",
    status: "pending",
    distance: "3.2 miles",
  },
  {
    id: "DEL-1002",
    customerName: "Sarah Johnson",
    address: "456 Oak Ave, Somewhere, CA 94124",
    deliveryTime: "1:00 PM - 3:00 PM",
    items: "1 large package",
    status: "pending",
    distance: "5.7 miles",
  },
  {
    id: "DEL-1003",
    customerName: "Michael Brown",
    address: "789 Pine Rd, Nowhere, CA 94125",
    deliveryTime: "3:30 PM - 5:30 PM",
    items: "3 packages",
    status: "accepted",
    distance: "2.1 miles",
  },
  {
    id: "DEL-1004",
    customerName: "Emily Davis",
    address: "101 Cedar Blvd, Elsewhere, CA 94126",
    deliveryTime: "9:00 AM - 11:00 AM",
    items: "1 package",
    status: "in_progress",
    distance: "4.5 miles",
  },
  {
    id: "DEL-1005",
    customerName: "Robert Wilson",
    address: "202 Maple Dr, Anywhere, CA 94127",
    deliveryTime: "11:30 AM - 1:30 PM",
    items: "2 packages",
    status: "passed",
    distance: "1.8 miles",
  },
  {
    id: "DEL-1006",
    customerName: "Jennifer Taylor",
    address: "303 Elm St, Someplace, CA 94128",
    deliveryTime: "2:00 PM - 4:00 PM",
    items: "4 packages",
    status: "failed",
    distance: "6.3 miles",
  },
];

export default function DeliveryList() {
  const [deliveries, setDeliveries] = useState<Delivery[]>(initialDeliveries);
  const [activeTab, setActiveTab] = useState<string>("all");
  const [searchTerm, setSearchTerm] = useState<string>("");

  // Update delivery status
  const updateDeliveryStatus = (id: string, newStatus: DeliveryStatus) => {
    setDeliveries(
      deliveries.map((delivery) =>
        delivery.id === id ? { ...delivery, status: newStatus } : delivery
      )
    );
  };

  // Filter deliveries based on active tab and search term
  const filteredDeliveries = deliveries.filter((delivery) => {
    const matchesTab = activeTab === "all" || delivery.status === activeTab;
    const matchesSearch =
      searchTerm === "" ||
      Object.values(delivery).some((value) =>
        value.toString().toLowerCase().includes(searchTerm.toLowerCase())
      );
    return matchesTab && matchesSearch;
  });

  // Get status badge color and text
  const getStatusBadge = (status: DeliveryStatus) => {
    switch (status) {
      case "pending":
        return (
          <Badge
            variant="outline"
            className="bg-yellow-50 text-yellow-700 border-yellow-200"
          >
            Pending
          </Badge>
        );
      case "accepted":
        return (
          <Badge
            variant="outline"
            className="bg-blue-50 text-blue-700 border-blue-200"
          >
            Accepted
          </Badge>
        );
      case "rejected":
        return (
          <Badge
            variant="outline"
            className="bg-red-50 text-red-700 border-red-200"
          >
            Rejected
          </Badge>
        );
      case "in_progress":
        return (
          <Badge
            variant="outline"
            className="bg-purple-50 text-purple-700 border-purple-200"
          >
            In Progress
          </Badge>
        );
      case "passed":
        return (
          <Badge
            variant="outline"
            className="bg-green-50 text-green-700 border-green-200"
          >
            Passed
          </Badge>
        );
      case "failed":
        return (
          <Badge
            variant="outline"
            className="bg-gray-50 text-gray-700 border-gray-200"
          >
            Failed
          </Badge>
        );
    }
  };

  return (
    <div className="container mx-auto px-4 py-6 max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Delivery Assignments</h1>
        <div className="flex items-center gap-2">
          <Badge className="bg-primary">{deliveries.length} Total</Badge>
          <Badge variant="outline" className="bg-yellow-50 text-yellow-700">
            {deliveries.filter((d) => d.status === "pending").length} Pending
          </Badge>
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
        <TabsList className="grid grid-cols-3 md:grid-cols-6 mb-4">
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="pending">Pending</TabsTrigger>
          <TabsTrigger value="accepted">Accepted</TabsTrigger>
          <TabsTrigger value="in_progress">In Progress</TabsTrigger>
          <TabsTrigger value="passed">Passed</TabsTrigger>
          <TabsTrigger value="failed">Failed</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="mt-0">
          <div className="grid gap-4">
            {filteredDeliveries.length > 0 ? (
              filteredDeliveries.map((delivery) => (
                <Card key={delivery.id} className="overflow-hidden">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-lg font-medium">
                        {delivery.id}
                      </CardTitle>
                      {getStatusBadge(delivery.status)}
                    </div>
                  </CardHeader>
                  <CardContent className="pb-3">
                    <div className="grid gap-3">
                      <div className="flex items-start gap-2">
                        <User className="h-4 w-4 mt-1 text-muted-foreground" />
                        <span className="font-medium">
                          {delivery.customerName}
                        </span>
                      </div>
                      <div className="flex items-start gap-2">
                        <MapPin className="h-4 w-4 mt-1 text-muted-foreground" />
                        <span className="text-sm text-muted-foreground">
                          {delivery.address}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4 text-muted-foreground" />
                          <span>{delivery.deliveryTime}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Truck className="h-4 w-4 text-muted-foreground" />
                          <span>{delivery.distance}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Package className="h-4 w-4 text-muted-foreground" />
                        <span className="text-sm">{delivery.items}</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="flex flex-wrap gap-2 pt-0">
                    {delivery.status === "pending" && (
                      <>
                        <Button
                          size="sm"
                          className="bg-green-600 hover:bg-green-700"
                          onClick={() =>
                            updateDeliveryStatus(delivery.id, "accepted")
                          }
                        >
                          <CheckCircle className="mr-1 h-4 w-4" /> Accept
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() =>
                            updateDeliveryStatus(delivery.id, "rejected")
                          }
                        >
                          <XCircle className="mr-1 h-4 w-4" /> Reject
                        </Button>
                      </>
                    )}

                    {delivery.status === "accepted" && (
                      <Button
                        size="sm"
                        className="bg-purple-600 hover:bg-purple-700"
                        onClick={() =>
                          updateDeliveryStatus(delivery.id, "in_progress")
                        }
                      >
                        <Truck className="mr-1 h-4 w-4" /> Start Delivery
                      </Button>
                    )}

                    {delivery.status === "in_progress" && (
                      <>
                        <Button
                          size="sm"
                          className="bg-green-600 hover:bg-green-700"
                          onClick={() =>
                            updateDeliveryStatus(delivery.id, "passed")
                          }
                        >
                          <ThumbsUp className="mr-1 h-4 w-4" /> Complete
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() =>
                            updateDeliveryStatus(delivery.id, "failed")
                          }
                        >
                          <ThumbsDown className="mr-1 h-4 w-4" /> Failed
                        </Button>
                      </>
                    )}

                    {(delivery.status === "passed" ||
                      delivery.status === "failed" ||
                      delivery.status === "rejected") && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() =>
                          updateDeliveryStatus(delivery.id, "pending")
                        }
                      >
                        Reset
                      </Button>
                    )}
                  </CardFooter>
                </Card>
              ))
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
