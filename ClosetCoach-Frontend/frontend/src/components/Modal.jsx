import { useEffect, useCallback } from "react";

const Modal = ({ isOpen, onClose, title, children }) => {
    // Handle ESC key to close modal
    const handleEscape = useCallback((e) => {
        if (e.key === "Escape") {
            onClose();
        }
    }, [onClose]);

    useEffect(() => {
        if (isOpen) {
            document.addEventListener("keydown", handleEscape);
            document.body.style.overflow = "hidden"; // Lock body scroll
        }
        return () => {
            document.removeEventListener("keydown", handleEscape);
            document.body.style.overflow = "unset";
        };
    }, [isOpen, handleEscape]);

    // Handle backdrop click
    const handleBackdropClick = (e) => {
        if (e.target.classList.contains("cc-modal-overlay")) {
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div className="cc-modal-overlay" onClick={handleBackdropClick}>
            <div className="cc-modal-container">
                {/* Modal Header */}
                <div className="cc-modal-header">
                    <h3 className="cc-modal-title">{title}</h3>
                    <button
                        className="cc-modal-close"
                        onClick={onClose}
                        aria-label="Close modal"
                    >
                        ✕
                    </button>
                </div>

                {/* Modal Content */}
                <div className="cc-modal-content">
                    {children}
                </div>
            </div>
        </div>
    );
};

export default Modal;
