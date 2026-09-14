import { useState, useEffect } from "react";
import { useAuth } from "../src/context/AuthContext";
import { db } from "../src/firebase";
import { collection, addDoc, getDocs, deleteDoc, doc, query, where } from "firebase/firestore";

const Wardrobe = () => {
    const { user } = useAuth();
    const [clothes, setClothes] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadForm, setUploadForm] = useState({
        category: "",
        color: "",
        name: ""
    });
    const [selectedImage, setSelectedImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    // Fetch user's clothes on mount
    useEffect(() => {
        if (user) {
            fetchClothes();
        }
    }, [user]);

    const fetchClothes = async () => {
        setIsLoading(true);
        try {
            const q = query(
                collection(db, "wardrobe"),
                where("userId", "==", user.uid)
            );
            const querySnapshot = await getDocs(q);
            const items = [];
            querySnapshot.forEach((doc) => {
                items.push({ id: doc.id, ...doc.data() });
            });
            setClothes(items);
        } catch (err) {
            setError("Failed to load your wardrobe");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    // Compress and convert image to base64
    const compressAndConvertToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    // Create canvas for compression
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');

                    // Calculate new dimensions (max 800px)
                    const maxSize = 800;
                    let width = img.width;
                    let height = img.height;

                    if (width > height && width > maxSize) {
                        height = (height * maxSize) / width;
                        width = maxSize;
                    } else if (height > maxSize) {
                        width = (width * maxSize) / height;
                        height = maxSize;
                    }

                    canvas.width = width;
                    canvas.height = height;

                    // Draw and compress
                    ctx.drawImage(img, 0, 0, width, height);

                    // Convert to base64 with compression (0.7 quality)
                    const base64 = canvas.toDataURL('image/jpeg', 0.7);
                    resolve(base64);
                };
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    };

    const handleImageSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            if (!file.type.startsWith("image/")) {
                setError("Please select an image file");
                return;
            }
            if (file.size > 5 * 1024 * 1024) {
                setError("Image must be less than 5MB");
                return;
            }
            setSelectedImage(file);
            const reader = new FileReader();
            reader.onloadend = () => setImagePreview(reader.result);
            reader.readAsDataURL(file);
            setError(null);
        }
    };

    const handleUpload = async () => {
        if (!selectedImage || !uploadForm.category || !uploadForm.name) {
            setError("Please fill in all required fields");
            return;
        }

        setIsUploading(true);
        setError(null);

        try {
            console.log("Starting upload...", { fileName: selectedImage.name, size: selectedImage.size });

            // Compress and convert image to base64
            console.log("Compressing and converting image to base64...");
            const base64Image = await compressAndConvertToBase64(selectedImage);
            console.log("Image converted, base64 length:", base64Image.length);

            // Check if base64 is within Firestore document limit (~1MB)
            if (base64Image.length > 900000) {
                setError("Image is too large even after compression. Please use a smaller image.");
                setIsUploading(false);
                return;
            }

            // Save to Firestore (both metadata and image data)
            console.log("Saving to Firestore...");
            await addDoc(collection(db, "wardrobe"), {
                userId: user.uid,
                name: uploadForm.name,
                category: uploadForm.category,
                color: uploadForm.color,
                imageUrl: base64Image,  // Store base64 directly as imageUrl
                createdAt: new Date().toISOString()
            });

            console.log("Success! Item added to wardrobe.");

            setSuccess("Item added to your wardrobe!");
            setSelectedImage(null);
            setImagePreview(null);
            setUploadForm({ category: "", color: "", name: "" });
            fetchClothes();

            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            console.error("Upload error:", err);

            if (err.code === 'permission-denied') {
                setError("Permission denied. Please make sure you're logged in.");
            } else if (err.message && err.message.includes('quota')) {
                setError("Storage quota exceeded. Please delete some items first.");
            } else {
                setError(`Upload failed: ${err.message || "Unknown error"}`);
            }
        } finally {
            setIsUploading(false);
        }
    };

    const handleDelete = async (item) => {
        if (!window.confirm(`Delete "${item.name}" from your wardrobe?`)) return;

        try {
            // Delete from Firestore only (no Storage to delete anymore)
            await deleteDoc(doc(db, "wardrobe", item.id));

            setClothes(clothes.filter(c => c.id !== item.id));
            setSuccess("Item removed from wardrobe");
            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            setError("Failed to delete item");
            console.error(err);
        }
    };

    const categories = [
        { value: "top", label: "Top" },
        { value: "pants", label: "Pants" },
        { value: "jacket", label: "Jacket" },
        { value: "dress", label: "Dress" },
        { value: "shoes", label: "Shoes" },
        { value: "accessory", label: "Accessory" }
    ];

    const colors = [
        { value: "black", label: "Black", hex: "#2b2b2b" },
        { value: "white", label: "White", hex: "#ffffff" },
        { value: "blue", label: "Blue", hex: "#3b82f6" },
        { value: "red", label: "Red", hex: "#ef4444" },
        { value: "green", label: "Green", hex: "#22c55e" },
        { value: "yellow", label: "Yellow", hex: "#ffc629" },
        { value: "pink", label: "Pink", hex: "#ec4899" },
        { value: "beige", label: "Beige", hex: "#d4a574" },
        { value: "gray", label: "Gray", hex: "#6b7280" },
        { value: "brown", label: "Brown", hex: "#92400e" }
    ];

    return (
        <main className="cc-wardrobe-page">
            {/* Header */}
            <section className="cc-wardrobe-header">
                <span className="cc-section-tag">Your Collection</span>
                <h1>My Wardrobe</h1>
                <p>Upload and manage your clothing items. Our AI will use these to create personalized outfits for you.</p>
            </section>

            {/* Messages */}
            {error && (
                <div className="cc-wardrobe-error">
                    <span>!</span> {error}
                </div>
            )}
            {success && (
                <div className="cc-wardrobe-success">
                    <span>✓</span> {success}
                </div>
            )}

            {/* Upload Section */}
            <section className="cc-wardrobe-upload-section">
                <h2>Add New Item</h2>
                <div className="cc-wardrobe-upload-form">
                    {/* Image Upload */}
                    <label className={`cc-wardrobe-image-upload ${imagePreview ? 'has-image' : ''}`}>
                        {imagePreview ? (
                            <div className="cc-wardrobe-preview-wrapper">
                                <img src={imagePreview} alt="Preview" />
                                <span className="cc-wardrobe-change-text">Click to change</span>
                            </div>
                        ) : (
                            <div className="cc-wardrobe-upload-placeholder">
                                <span className="cc-upload-icon">+</span>
                                <span>Click to upload image</span>
                                <span className="cc-upload-hint">Max 5MB</span>
                            </div>
                        )}
                        <input
                            type="file"
                            hidden
                            accept="image/*"
                            onChange={handleImageSelect}
                        />
                    </label>

                    {/* Form Fields */}
                    <div className="cc-wardrobe-form-fields">
                        <div className="cc-wardrobe-field">
                            <label>Item Name *</label>
                            <input
                                type="text"
                                placeholder="e.g., Blue Cotton Shirt"
                                value={uploadForm.name}
                                onChange={(e) => setUploadForm({ ...uploadForm, name: e.target.value })}
                            />
                        </div>

                        <div className="cc-wardrobe-field">
                            <label>Category *</label>
                            <div className="cc-wardrobe-category-grid">
                                {categories.map(cat => (
                                    <button
                                        key={cat.value}
                                        className={`cc-wardrobe-category-btn ${uploadForm.category === cat.value ? 'active' : ''}`}
                                        onClick={() => setUploadForm({ ...uploadForm, category: cat.value })}
                                    >
                                        <span>{cat.label}</span>
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="cc-wardrobe-field">
                            <label>Primary Color</label>
                            <div className="cc-wardrobe-color-grid">
                                {colors.map(color => (
                                    <button
                                        key={color.value}
                                        className={`cc-wardrobe-color-btn ${uploadForm.color === color.value ? 'active' : ''}`}
                                        style={{ backgroundColor: color.hex }}
                                        onClick={() => setUploadForm({ ...uploadForm, color: color.value })}
                                        title={color.label}
                                    />
                                ))}
                            </div>
                        </div>

                        <button
                            className={`cc-primary-btn cc-wardrobe-add-btn ${isUploading ? 'loading' : ''}`}
                            onClick={handleUpload}
                            disabled={isUploading || !selectedImage || !uploadForm.category || !uploadForm.name}
                        >
                            {isUploading ? (
                                <>
                                    <span className="cc-spinner"></span>
                                    Uploading...
                                </>
                            ) : (
                                "Add to Wardrobe"
                            )}
                        </button>
                    </div>
                </div>
            </section>

            {/* Wardrobe Grid */}
            <section className="cc-wardrobe-grid-section">
                <h2>Your Clothes ({clothes.length})</h2>

                {isLoading ? (
                    <div className="cc-wardrobe-loading">
                        <span className="cc-spinner"></span>
                        <span>Loading your wardrobe...</span>
                    </div>
                ) : clothes.length === 0 ? (
                    <div className="cc-wardrobe-empty">
                        <div className="cc-empty-icon"></div>
                        <h3>Your wardrobe is empty</h3>
                        <p>Start by uploading some of your favorite clothes above!</p>
                    </div>
                ) : (
                    <div className="cc-wardrobe-grid">
                        {clothes.map(item => (
                            <div key={item.id} className="cc-wardrobe-card">
                                <div className="cc-wardrobe-card-image">
                                    <img src={item.imageUrl} alt={item.name} />
                                    <button
                                        className="cc-wardrobe-delete-btn"
                                        onClick={() => handleDelete(item)}
                                        title="Delete item"
                                    >
                                        ×
                                    </button>
                                </div>
                                <div className="cc-wardrobe-card-info">
                                    <span className="cc-wardrobe-card-name">{item.name}</span>
                                    <div className="cc-wardrobe-card-meta">
                                        <span className="cc-wardrobe-card-category">
                                            {item.category}
                                        </span>
                                        {item.color && (
                                            <span
                                                className="cc-wardrobe-card-color"
                                                style={{ backgroundColor: colors.find(c => c.value === item.color)?.hex }}
                                            />
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </section>
        </main>
    );
};

export default Wardrobe;
