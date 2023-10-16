"use client";
import React, { useState, useEffect } from "react";
import axios from "@/api/axiosInstance";
import { Truck } from "@/model/Truck";
import { FoodItem } from "@/model/FoodItem";

export default function Home() {
  const [trucks, setTrucks] = useState<Truck[]>([]);
  const [foodItems, setFoodItems] = useState<FoodItem[]>([]);
  const [totalAmount, setTotalAmount] = useState<number>(0);
  const [selectedTruckId, setSelectedTruckId] = useState<string | null>(null);
  const [quantity, setQuantity] = useState<number>(1);
  const [selectedFoodItem, setSelectedFoodItem] = useState<number | null>(null);

  const fetchTrucks = async () => {
    try {
      const response = await axios.get("/truck");
      if (response.status === 200) {
        const data = response.data.trucks;
        setTrucks(data);
      } else {
        console.error("Failed to fetch trucks.");
      }
    } catch (error) {
      console.error("Error fetching trucks:", error);
    }
  };

  const fetchTruckData = async (truckId: string) => {
    try {
      const response = await axios.get(`/truck/${truckId}`);
      if (response.status === 200) {
        const data = response.data;
        setFoodItems(data.food_items);
        setTotalAmount(data.total_amount);
      } else {
        console.error("Failed to fetch truck data.");
      }
    } catch (error) {
      console.error("Error fetching truck data:", error);
    }
  };

  const handleTruckSelection = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const selectedId = event.target.value;
    setSelectedTruckId(selectedId);

    if (selectedId) {
      fetchTruckData(selectedId);
    }
  };

  const handleOrderSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (selectedTruckId && selectedFoodItem && quantity > 0) {
      try {
        const response = await axios.post("/order/", {
          quantity: quantity,
          food_item: selectedFoodItem,
          truck: selectedTruckId,
        });
        if (response.status === 200) {
          alert(response.data.message);
          fetchTruckData(selectedTruckId);
        }
      } catch (error) {
        alert("SORRY!");
        console.error("Error placing the order:", error);
      }
    }
  };

  useEffect(() => {
    fetchTrucks();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-semibold mb-4">
        Welcome to Ice Cream Truck
      </h1>

      <div className="w-1/3">
        <select
          className="w-full border rounded p-2"
          onChange={handleTruckSelection}
          value={selectedTruckId || ""}
        >
          <option value="">Select a Truck</option>
          {trucks.map((truck) => (
            <option key={truck.id} value={truck.id}>
              {truck.name}
            </option>
          ))}
        </select>
      </div>
      <div className="my-4">
        <h2 className="text-2xl font-semibold">Total Amount: {totalAmount}</h2>
      </div>
      <div className="my-4">
        <h2 className="text-2xl font-semibold">Food Items:</h2>
        <ul>
          {foodItems.map((foodItem) => (
            <li key={foodItem.id} className="mt-2">
              <div className="flex justify-between items-center">
                <span className="text-lg">{foodItem.name}</span>
                <span className="text-gray-600">
                  Price: ${foodItem.price.toFixed(2)}, Quantity:{" "}
                  {foodItem.quantity}
                </span>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h2 className="text-2xl font-semibold">Place an Order:</h2>
        <form onSubmit={handleOrderSubmit} className="w-1/3">
          <div className="mb-4">
            <label className="block text-gray-600">Quantity:</label>
            <input
              type="number"
              className="w-full border rounded p-2"
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-600">Food Item:</label>
            <select
              className="w-full border rounded p-2"
              value={selectedFoodItem || ""}
              onChange={(e) => setSelectedFoodItem(Number(e.target.value))}
            >
              <option value="">Select a Food Item</option>
              {foodItems.map((foodItem) => (
                <option key={foodItem.id} value={foodItem.id}>
                  {foodItem.name}
                </option>
              ))}
            </select>
          </div>
          <button
            type="submit"
            className="bg-blue-500 text-white rounded p-2 hover:bg-blue-700"
          >
            Place Order
          </button>
        </form>
      </div>
    </div>
  );
}
