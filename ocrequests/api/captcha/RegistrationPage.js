const readImage = async () => {
  const img = document.getElementById("capt");

  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  // Set canvas dimensions to match the image
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;

  // Draw the image onto the canvas
  ctx.drawImage(img, 0, 0);

  // Convert canvas to PNG binary
  const blob = await blobToString(
    await canvas.toBlob((pngBlob) => pngBlob, "image/png")
  );
  console.log(blob);
};

const blobToString = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    // Set up the onload event to resolve the promise with the result
    reader.onload = () => {
      resolve(reader.result);
    };

    // Set up the onerror event to reject the promise in case of an error
    reader.onerror = () => {
      reject(new Error("Failed to read blob as string."));
    };

    // Read the blob as text
    reader.readAsDataURL(blob);
  });
};
