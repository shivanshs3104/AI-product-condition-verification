const ENDPOINT = "/api/upload-image";

export async function uploadImage(file) {
  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch(ENDPOINT, {
    method: "POST",
    body: formData
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.error || "Image upload failed.");
  }

  return payload;
}
