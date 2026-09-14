import { useState, useEffect } from "react";
import { useAuth } from "../src/context/AuthContext";
import { db } from "../src/firebase";
import { collection, query, where, getDocs, deleteDoc, doc } from "firebase/firestore";

const SavedLooks = () => {
    const { user } = useAuth();
    const [savedLooks, setSavedLooks] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [deletingId, setDeletingId] = useState(null);

    useEffect(() => {
        if (user) {
            fetchSavedLooks();
        }
    }, [user]);

    const fetchSavedLooks = async () => {
        setIsLoading(true);
        try {
            const q = query(
                collection(db, "savedLooks"),
                where("userId", "==", user.uid)
            );
            const snapshot = await getDocs(q);
            const looks = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
            // Sort by date (newest first)
            looks.sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt));
            setSavedLooks(looks);
        } catch (err) {
            console.error("Failed to fetch saved looks:", err);
            setError("Failed to load your saved looks");
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (lookId) => {
        if (!window.confirm("Delete this saved look?")) return;

        setDeletingId(lookId);
        try {
            await deleteDoc(doc(db, "savedLooks", lookId));
            setSavedLooks(savedLooks.filter(look => look.id !== lookId));
        } catch (err) {
            console.error("Failed to delete look:", err);
            setError("Failed to delete this look");
        } finally {
            setDeletingId(null);
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    };

    return (
        <main className="cc-saved-looks-page">
            <section className="cc-saved-looks-header">
                <span className="cc-section-tag">Your Collection</span>
                <h1>Saved Looks</h1>
                <p>Your favorite outfit combinations saved for quick reference.</p>
            </section>

            {error && (
                <div className="cc-wardrobe-error">
                    <span>!</span> {error}
                </div>
            )}

            {isLoading ? (
                <div className="cc-wardrobe-loading">
                    <span className="cc-spinner"></span>
                    <span>Loading your saved looks...</span>
                </div>
            ) : savedLooks.length === 0 ? (
                <div className="cc-saved-looks-empty">
                    <div className="cc-empty-icon">💫</div>
                    <h3>No Saved Looks Yet</h3>
                    <p>Generate an outfit using Outfit Generator or Complete Your Look, then save it to see it here!</p>
                    <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
                        <a href="/outfit-generator" className="cc-primary-btn">
                            Outfit Generator
                        </a>
                        <a href="/cir" className="cc-secondary-btn">
                            Complete Your Look
                        </a>
                    </div>
                </div>
            ) : (
                <div className="cc-saved-looks-grid">
                    {savedLooks.map(look => (
                        <div key={look.id} className="cc-saved-look-card">
                            <button
                                className="cc-saved-look-delete"
                                onClick={() => handleDelete(look.id)}
                                disabled={deletingId === look.id}
                                title="Delete this look"
                            >
                                {deletingId === look.id ? '...' : '×'}
                            </button>

                            <div className="cc-saved-look-images">
                                {/* Uploaded Item */}
                                {look.uploadedItem?.imageBase64 && (
                                    <div className="cc-saved-look-item">
                                        <img
                                            src={look.uploadedItem.imageBase64}
                                            alt="Your item"
                                        />
                                        <span className="cc-saved-look-label">
                                            {look.uploadedItem.category === 'top' ? 'Top' : 'Bottom'}
                                        </span>
                                    </div>
                                )}

                                {/* Plus Sign */}
                                {look.matchedItems?.length > 0 && (
                                    <span className="cc-saved-look-plus">+</span>
                                )}

                                {/* Matched Items */}
                                {look.matchedItems?.map((item, idx) => (
                                    <div key={idx} className="cc-saved-look-item">
                                        {item.imageBase64 && (
                                            <img
                                                src={item.imageBase64.startsWith('data:')
                                                    ? item.imageBase64
                                                    : `data:image/jpeg;base64,${item.imageBase64}`
                                                }
                                                alt={item.category}
                                            />
                                        )}
                                        <span className="cc-saved-look-label">{item.category}</span>
                                    </div>
                                ))}
                            </div>

                            <div className="cc-saved-look-meta">
                                <div className="cc-saved-look-tags">
                                    {look.preferences?.occasion && (
                                        <span className="cc-saved-look-tag">{look.preferences.occasion}</span>
                                    )}
                                    {look.preferences?.mood && (
                                        <span className="cc-saved-look-tag">{look.preferences.mood}</span>
                                    )}
                                    {look.preferences?.weather && (
                                        <span className="cc-saved-look-tag">{look.preferences.weather}</span>
                                    )}
                                </div>
                                <span className="cc-saved-look-date">
                                    Saved {formatDate(look.savedAt)}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </main>
    );
};

export default SavedLooks;
