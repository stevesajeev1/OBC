import { user } from "@/state";

// TODO: Replace with actual logic to get profile
export const getProfile = () => {
  if (user.value === null) return;

  return {
    name: "John Doe",
    image_url: "https://cdn.vectorstock.com/i/500p/29/52/faceless-male-avatar-in-hoodie-vector-56412952.jpg"
  }
}