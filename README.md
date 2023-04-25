# MissingPreviewFetcher (not ready)
My project is a sdwebui extension that solves the problem of the endless LoRA sitting in our folders with paired images
I see that many people have this issue
so I tried to come up with an extension that
1. scans the LoRA folder for files with no image counterpart
2. scans the user's desired img output folder's images' metadata
3. compares the names that it has saved in part 1 of the lonely LoRA and the metadata in step 2, then it pairs randomly images with LoRA, it takes one, renames it, and puts it in the LoRA folder

It fetches missing preview images for LoRA cards
