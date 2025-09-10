import json
import os
from PIL import Image, ImageDraw


def main():
    fp = "PolymerLit-OA_raw_images"
    ofp = "PolymerLit-OA_processed"

    sources = [
        # generic
        ("generic/acspolymersau", "generic/acspolymersau_labels.json"),
        ("generic/acsmacrolett", "generic/acsmacrolett_labels.json"),
        ("generic/macromolecules", "generic/macromolecules_labels.json"),
        # ladder
        ("ladder/acsmacrolett", "ladder/ladder_all_labels.json"),
        ("ladder/angewchemie", "ladder/ladder_all_labels.json"),
        ("ladder/chemengjournal", "ladder/ladder_all_labels.json"),
        ("ladder/chemicalscience", "ladder/ladder_all_labels.json"),
        ("ladder/digitaldiscovery", "ladder/ladder_all_labels.json"),
        ("ladder/faradaydiscussions", "ladder/ladder_all_labels.json"),
        ("ladder/macromolecules", "ladder/ladder_all_labels.json"),
        ("ladder/polymer", "ladder/ladder_all_labels.json"),
    ]

    for source, label_file in sources:
        label_file = os.path.join(fp, label_file)
        with open(label_file, "r") as f:
            labels = json.load(f)

        image_id2fn = {}
        image_file_count = 0
        for image_metadata in labels["images"]:
            image_id = image_metadata["id"]
            image_fn = image_metadata["file_name"]
            image_fn_full = os.path.join(fp, source, image_fn)

            if not os.path.exists(image_fn_full):
                # print(f"{image_fn_full} not found, skipping...")
                continue

            image_id2fn[image_id] = {
                "file_name": image_fn,
                "sub_image_index": 1
            }
            image_file_count += 1

        print(f"Total images in labels: {len(labels['images'])}, found {image_file_count}")

        os.makedirs(os.path.join(ofp, source), exist_ok=True)
        for annotation in labels["annotations"]:
            try:
                image_fn = image_id2fn[annotation["image_id"]]["file_name"]
            except KeyError:
                continue
            sub_image_index = image_id2fn[annotation["image_id"]]["sub_image_index"]

            image_fn_full = os.path.join(fp, source, image_fn)
            # for ladder, the single labels file should cover every image
            # we can afford some redundancy by iterating over all sources
            # if not os.path.exists(image_fn_full):
            #     continue

            basenames = image_fn.split(".")
            basename = ".".join(basenames[:-1])
            image_ofn = os.path.join(ofp, source, f"{basename}_{sub_image_index}.png")

            img = Image.open(image_fn_full)
            width, height = img.size

            # Polygon segmentation (single or multi-part)
            segmentation = annotation["segmentation"]

            # Create binary mask
            mask = Image.new("L", (width, height), 0)
            for polygon in segmentation:
                ImageDraw.Draw(mask).polygon(polygon, outline=255, fill=255)

            # Composite the image with white background
            white_bg = Image.new("RGB", img.size, (255, 255, 255))
            masked_img = Image.composite(img, white_bg, mask)

            # Apply mask
            # masked_img = Image.composite(img, Image.new("RGB", img.size), mask)

            # Optionally crop to tight bbox around mask
            # mask_np = np.array(mask)
            # ys, xs = np.where(mask_np)
            # x1, y1, x2, y2 = xs.min(), ys.min(), xs.max(), ys.max()
            # cropped_masked_img = masked_img.crop((x1, y1, x2, y2))
            # cropped_masked_img.save('cropped_segmentation.jpg')

            bbox = annotation["bbox"]
            x1 = bbox[0]
            y1 = bbox[1]
            x2 = x1 + bbox[2]
            y2 = y1 + bbox[3]

            cropped_masked_img = masked_img.crop((x1, y1, x2, y2))
            cropped_masked_img.save(image_ofn)

            image_id2fn[annotation["image_id"]]["sub_image_index"] += 1


if __name__ == "__main__":
    main()
