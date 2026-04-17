"""
Demo script for Nano Banana Model.

Author: Chandan Kumar
Email: chandan@bit.edu.cn
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from nano_banana import NanoBananaModel, BananaFeatures


def run_demo():
    """Run demonstration of the Nano Banana Model."""
    print("\n" + "=" * 70)
    print(" " * 15 + "🍌 Nano Banana Model Demo 🍌")
    print("=" * 70)
    print("\nAuthor: Chandan Kumar")
    print("Email: chandan@bit.edu.cn")
    print("GitHub: https://github.com/yourusername/nano-banana-project")
    print("-" * 70)

    # Initialize model
    model = NanoBananaModel(threshold=0.5)

    # Example bananas with different ripeness levels
    bananas = [
        {
            "name": "Green Banana (Unripe)",
            "features": BananaFeatures(
                length_cm=12.5,
                diameter_cm=2.8,
                color_score=0.15,  # Very green
                weight_grams=95.0,
                firmness=7.5,
                temperature_celsius=20.0
            )
        },
        {
            "name": "Perfect Yellow Banana (Ripe)",
            "features": BananaFeatures(
                length_cm=16.0,
                diameter_cm=3.2,
                color_score=0.55,  # Bright yellow
                weight_grams=130.0,
                firmness=4.0,
                temperature_celsius=22.0
            )
        },
        {
            "name": "Brown-Spotted Banana (Overripe)",
            "features": BananaFeatures(
                length_cm=18.5,
                diameter_cm=3.8,
                color_score=0.85,  # Brown spots
                weight_grams=160.0,
                firmness=2.0,
                temperature_celsius=25.0
            )
        }
    ]

    # Analyze each banana
    print("\n📊 Analysis Results:\n")
    for banana in bananas:
        print(f"{banana['name']}:")
        print("-" * 70)
        result = model.analyze(banana['features'])

        status_emoji = {
            "unripe": "🌿",
            "ripe": "🍌",
            "overripe": "🤢"
        }

        print(f"  Status: {status_emoji.get(result['status'], '❓')} {result['status'].upper()}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Volume: {result['volume_cm3']} cm³")
        print(f"  Density: {result['density_g_per_cm3']} g/cm³")
        print(f"  Weight: {result['features']['weight_grams']} g")
        print(f"  Length: {result['features']['length_cm']} cm")
        print(f"  Diameter: {result['features']['diameter_cm']} cm")
        print(f"  Color Score: {result['features']['color_score']:.2f}")
        print(f"  Firmness: {result['features']['firmness']}")
        print(f"  Temperature: {result['features']['temperature_celsius']}°C")
        print()

    # Batch processing example
    print("\n📦 Batch Processing Example:")
    print("-" * 70)
    all_bananas = [b['features'] for b in bananas]
    batch_results = model.batch_analyze(all_bananas)
    print(f"  Processed {len(batch_results)} bananas")
    status_counts = {}
    for r in batch_results:
        status = r['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    for status, count in status_counts.items():
        print(f"  {status.capitalize()}: {count}")
    print()

    print("=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70)
    print("\nFor more information, see:")
    print("  - README.md")
    print("  - docs/FLOWCHART.md")
    print("  - https://github.com/yourusername/nano-banana-project")
    print()


if __name__ == "__main__":
    run_demo()
