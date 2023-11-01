"use client";
import React, { useState, useEffect } from "react";
import axios from "@/api/axiosInstance";
import { Truck } from "@/model/Truck";
import { FoodItem } from "@/model/FoodItem";
import { Flavor } from "@/model/Flavor";
import { FoodItemType } from "@/model/FoodItemType";

export default function Home() {
  const [trucks, setTrucks] = useState<Truck[]>([]);
  const [flavors, setFlavors] = useState<Flavor[]>([]);
  const [foodItemTypes, setFoodItemTypes] = useState<FoodItemType[]>([]);
  const [foodItems, setFoodItems] = useState<FoodItem[]>([]);
  const [totalAmount, setTotalAmount] = useState<number>(0);
  const [selectedTruckId, setSelectedTruckId] = useState<number | null>(null);
  const [quantity, setQuantity] = useState<number>(1);
  const [selectedFoodItemTypeId, setSelectedFoodItemTypeId] = useState<
    number | null
  >(null);
  const [selectedFlavorId, setSelectedFlavorId] = useState<number | null>(null);

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

  const fetchFlavors = async () => {
    try {
      const response = await axios.get("/flavor");
      if (response.status === 200) {
        const data = response.data.flavors;
        setFlavors(data);
      } else {
        console.error("Failed to fetch flavors.");
      }
    } catch (error) {
      console.error("Error fetching flavors:", error);
    }
  };

  const fetchFoodItemTypes = async () => {
    try {
      const response = await axios.get("/food-item-type");
      if (response.status === 200) {
        const data = response.data.food_item_types;
        setFoodItemTypes(data);
      } else {
        console.error("Failed to fetch food item types.");
      }
    } catch (error) {
      console.error("Error fetching food item types:", error);
    }
  };

  const fetchTruckData = async (truckId: number) => {
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
    const selectedId = +event.target.value;
    setSelectedTruckId(selectedId);

    if (selectedId) {
      fetchTruckData(selectedId);
    }
  };

  const handleOrderSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (selectedTruckId && selectedFoodItemTypeId && quantity > 0) {
      try {
        const response = await axios.post("/order/", {
          quantity: quantity,
          food_item_type_id: selectedFoodItemTypeId,
          flavor_id: selectedFlavorId !== null ? selectedFlavorId : 0,
          truck_id: selectedTruckId,
        });
        if (response.status === 200) {
          alert(response.data.message);
          fetchTruckData(selectedTruckId);
        }
      } catch (error: any) {
        alert(error.response.data.message);
        console.error("Error placing the order:", error);
      }
    }
  };

  useEffect(() => {
    fetchTrucks();
    fetchFlavors();
    fetchFoodItemTypes();
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
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2">
          <div className="grid grid-cols-3 gap-4">
            {foodItems.map((foodItem) => (
              <div
                key={foodItem.id}
                className="bg-pink-100 p-4 rounded-lg shadow-md"
              >
                <h3 className="text-lg font-semibold mb-2">
                  {foodItem.flavor
                    ? foodItem.flavor + " " + foodItem.type
                    : foodItem.type}
                </h3>
                <p className="mb-2">
                  <strong>Quantity:</strong> {foodItem.quantity}
                </p>
                <p className="mb-2">
                  <strong>Price:</strong> {foodItem.price}
                </p>
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="bg-gray-100 p-4 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold">Place an Order:</h2>
            <form onSubmit={handleOrderSubmit}>
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
                <label className="block text-gray-600">Food Item Type:</label>
                <select
                  className="w-full border rounded p-2"
                  value={selectedFoodItemTypeId || ""}
                  onChange={(e) =>
                    setSelectedFoodItemTypeId(Number(e.target.value))
                  }
                >
                  <option value="">Select a Food Item Type</option>
                  {foodItemTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-gray-600">Flavor:</label>
                {selectedFoodItemTypeId !== null ? (
                  foodItemTypes.find(
                    (type) => type.id === selectedFoodItemTypeId
                  )?.has_flavor ? (
                    <select
                      className="w-full border rounded p-2"
                      value={selectedFlavorId || ""}
                      onChange={(e) =>
                        setSelectedFlavorId(Number(e.target.value))
                      }
                    >
                      <option value="">Select a Flavor</option>
                      {flavors.map((flavor) => (
                        <option key={flavor.id} value={flavor.id}>
                          {flavor.name}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <p>No flavors available for this food item type.</p>
                  )
                ) : (
                  <p>Please select a Food Item Type first.</p>
                )}
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
      </div>
    </div>
  );
}
