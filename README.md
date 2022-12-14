# librewords
Word cloud generation from different sources.

Inspired by video from Veritasium: [The Illusion of Truth](https://youtu.be/cebFWOlx848)

# Preparation

To install required packages run:

`pip3 install -r requirements.txt`

Heavy `tessdata` submodule is required for `document_to_cloud.py` only so you may not need it.

Also, you may need to install ffmpeg to use `speech_to_cloud.py` and `video_to_cloud.py`.

**And also**, `speech_to_cloud.py` and `video_to_cloud.py` make use of thirdparty server in order to translate speech into text.

# Usage:
`url_to_cloud.py -u "https://en.wikipedia.org/wiki/Manufacturing_Consent" -o manufacturing_consent.png`

**Note:** for now the first time using language different from English will take really long because of installing translation packages.

**Result:**

![sample result](example_result.png "result from running command")
