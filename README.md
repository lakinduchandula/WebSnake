# WebSnake
**WebSnake** is an automated web exploration and capture tool built with Python. It navigates to webpages, captures full-page screenshots with automatically-numbered filenames, and maintains a consistent naming convention for all captured images.

## How It Works

### Screenshot Naming & Configuration
WebSnake uses a `sites.json` configuration file to manage screenshot naming:

```json
{
  "exam_family": "GH-900",
  "topic_number": 1,
  "last_question": 8
}
```

Screenshots are saved with the format: **`{exam_family}-{topic_number}-{last_question}.png`**

For example, with the above config, the first screenshot would be named: `GH-900-1-8.png`

### Automatic Increment
After each screenshot is captured:
1. The `last_question` counter automatically increments by 1
2. The updated config is saved back to `sites.json`
3. The next screenshot will use the new counter value

So the next screenshot would be: `GH-900-1-9.png`, then `GH-900-1-10.png`, and so on.

### Infinite Loop
The script runs in a continuous loop:
1. Prompts you to enter a website URL
2. Captures a full-page screenshot with an auto-incremented filename
3. Updates the configuration file
4. Asks for the next URL

**Exit the loop** by typing `quit`, `exit`, or `q` when prompted for a URL.

## Use Case

WebSnake is particularly useful for **capturing exam questions from [examtopics.com](https://www.examtopics.com/)**. By maintaining consistent naming conventions and automatic numbering, it allows you to systematically collect and organize screenshots of exam questions for reference and study purposes.

Example workflow:
- Navigate to exam questions on examtopics.com
- Capture each question page with a single URL entry
- Screenshots are automatically named and numbered (e.g., `GH-900-1-8.png`, `GH-900-1-9.png`, etc.)
- Build an organized library of exam questions with zero manual naming effort

## Usage

Run the script:
```bash
python main.py
```

Then enter URLs as prompted:
```
Enter website URL (or 'quit' to exit): https://example.com
```

The screenshot will be saved to the `screenshots/` directory with an auto-numbered filename, and the counter will increment automatically for the next capture.

## Future Enhancements
WebSnake can evolve into an autonomous browser agent capable of searching the web, visiting pages, and extracting information automatically.
