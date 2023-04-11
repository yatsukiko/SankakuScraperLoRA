# SankakuScraperLoRA

This is a small Node.js application for scraping images from chan.sankakucomplex using Octoparse and preparing a dataset for the LoRA model.

This tool extracts images and tags from search query then outputs them to `/dataset/{number of steps}_{name of dataset}` as numeric file names and .txt with tags in them.

## Prerequisites

Before running this application, you will need to install Octoparse and load the provided template file. You will also need to change the login and password in Octoparse and update the URL for scraping.
[more information about octoparse usage here](https://github.com/yatsukiko/SankakuScraperLoRA/blob/main/octoparse.md)

## Getting Started

1. Clone this repository to your local machine.
2. In Octoparse, start the scraping process and extract data as a `.json` file. If unsure go back to [here](https://github.com/yatsukiko/SankakuScraperLoRA/blob/main/octoparse.md)
3. Place the `{result}.json` file next to `main.js`.
4. Run `npm i` to install dependencies.
5. Run `node main.js`.
6. If the `result.json` file is located next to `main.js` and the file name was not changed, you should be able to just press enter. Otherwise, specify the file name/location.
7. Next, it will ask you for the dataset name. Just input the name you want to train.
8. The script will first parse the `.json` file by filtering out empty `img_src` and then pretty print it. After that, it will start to download all images and place them into `/dataset/{number of steps}_{name of dataset}`.
9. Verify downloaded images, make sure there is no empty images or sankaku's expired link images (shouldn't happen if u downloaded them straight after scraping)
10. Go train a model or smth.

## Important Notes

- It is best to run `main.js` immediately after scraping all the images, as the URL to these images is based on a token that expires. If you try to run the script after about 30 minutes, it might not work.
- This script is based on the dataset parameters contained in this video: [https://www.youtube.com/watch?v=70H03cv57-o](https://www.youtube.com/watch?v=70H03cv57-o). If you have no idea what you are doing, please check out this video.
- The free version of chan.sankakucomplex allows only up to 25 pages, which is technically a maximum of 500 images (since each page contains 20 posts).
- The Octoparse template fails to scrape videos, instead it makes img_src empty but writes the tags, this is somewhat ok behaviour as you can't train via videos anyway (i think?).
- I cannot guarantee that this script will work with idol.sankakucomplex, go try it, I need to sleep.
- small importance, big chunk of this code (and this readme.md) was written by ChatGPT and then refactored by me, I do have some idea what I'm doing tho. 

## "Roadmap"
- refactor code, its not too bad but I think it can be done better
- make it more customizable/flexible, maybe other website or try scraping more.
- try to do everything in node.js instead of using Octoparse
- u tell me
