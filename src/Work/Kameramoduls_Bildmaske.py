import cv2
import os
import numpy as np

def load_images():
    # Originalbild und Maskenbild mit deinen Pfaden
    original_image_path = "/home/pi/FE_2025/Work/Bilder_machen/Bilder/Weg_vor_auto_04.01.2025.png"
    mask_image_path = "/home/pi/FE_2025/Work/Bilder_machen/Bilder/Weg_vor_auto_04.01.2025_Mask_whiteground2.png"

    # Prüfen, ob die Dateien existieren
    if not os.path.exists(original_image_path):
        print(f"Fehler: Originalbild '{original_image_path}' wurde nicht gefunden.")
        return None, None
    if not os.path.exists(mask_image_path):
        print(f"Fehler: Maskenbild '{mask_image_path}' wurde nicht gefunden.")
        return None, None

    # Bilder laden
    original = cv2.imread(original_image_path)
    mask = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)  # Als Graustufen laden

    if original is None:
        print("Fehler beim Laden des Originalbildes.")
        return None, None
    if mask is None:
        print("Fehler beim Laden des Maskenbildes.")
        return None, None

    # Größe der Maske an das Originalbild anpassen
    mask = cv2.resize(mask, (original.shape[1], original.shape[0]))

    return original, mask

def apply_custom_mask(original, mask):
    # **Keine Invertierung mehr!**

    # Normiere die Maske auf [0, 1]
    normalized_mask = mask / 255.0

    # Maske direkt auf das Originalbild anwenden
    masked_image_color = np.uint8(original * normalized_mask[:, :, None])

    return masked_image_color

def main():
    # Bilder laden
    original, mask = load_images()
    if original is None or mask is None:
        return

    # Maske anwenden
    masked_image_color = apply_custom_mask(original, mask)

    # Zeige das Originalbild, die Maske und das Ergebnis (ohne Invertierung)
    cv2.imshow("Originalbild", original)
    cv2.imshow("Maske auf Originalbild", masked_image_color)

    # Warte, bis eine Taste gedrückt wird
    print("Drücke 'q', um die Fenster zu schließen.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fenster schließen
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
