import unittest
import numpy as np
from PIL import Image
from stenciled import posterize_image, get_unique_colors, create_mask, trace_mask


class TestStenciled(unittest.TestCase):
    def setUp(self):
        # Create a simple test image (RGB)
        self.test_img = Image.new("RGB", (10, 10), "red")
        for i in range(5):
            for j in range(5):
                self.test_img.putpixel((i, j), (0, 255, 0))  # Green block

    def test_posterize_image(self):
        # Test posterization with 2 colors
        posterized = posterize_image(self.test_img, 2)
        self.assertEqual(posterized.mode, "P")
        self.assertLessEqual(len(get_unique_colors(posterized)), 2)

    def test_get_unique_colors(self):
        # Test unique color extraction
        posterized = posterize_image(self.test_img, 2)
        unique_colors = get_unique_colors(posterized)
        self.assertGreaterEqual(len(unique_colors), 1)

    def test_create_mask(self):
        # Test mask creation for a specific color index
        posterized = posterize_image(self.test_img, 2)
        unique_colors = get_unique_colors(posterized)
        mask = create_mask(posterized, unique_colors[0])
        self.assertEqual(mask.shape, (10, 10))
        # Ensure mask contains white pixels
        self.assertTrue(np.any(mask == 255))

    def test_trace_mask(self):
        # Test contour tracing and simplification
        posterized = posterize_image(self.test_img, 2)
        unique_colors = get_unique_colors(posterized)
        mask = create_mask(posterized, unique_colors[0])
        contours = trace_mask(mask, 0.01)
        self.assertIsInstance(contours, list)
        self.assertTrue(all(isinstance(c, np.ndarray) for c in contours))


if __name__ == "__main__":
    unittest.main()
