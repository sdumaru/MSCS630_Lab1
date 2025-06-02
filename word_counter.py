import threading
from collections import Counter
import sys
import re

# Regular expression to match words (letters and apostrophes)
WORD_RE = re.compile(r"\b[a-zA-Z']+\b")

def normalize(text):
    """
    Convert text to a list of lowercase words using the WORD_RE pattern.
    This handles punctuation by only capturing valid word characters.
    """
    return [w.lower() for w in WORD_RE.findall(text)]

def count_words(segment, result, index):
    """
    Worker function for each thread.
    - segment: a string containing the words to count
    - result: shared list where each thread stores its Counter
    - index: the position in `result` to store this thread's Counter
    """
    words = normalize(segment)               # Tokenize & normalize the segment
    word_count = Counter(words)             # Count occurrences in this segment
    result[index] = word_count              # Store intermediate result
    print(f"[Thread {index+1}] intermediate count: {dict(word_count)}")

def divide_text(text, num_threads):
    """
    Split the full text into num_threads parts (by word count).
    Returns a list of string segments.
    """
    words = normalize(text)                         # Tokenize & normalize entire text
    total_length = len(words)                       # Total number of words
    seg_len = total_length // num_threads           # Base size of each segment
    segments = []

    for i in range(num_threads):
        start_index = i * seg_len
        # Last segment takes any remaining words
        if i == num_threads - 1:
            end_index = None
        else:
            end_index =  (i + 1) * seg_len
        segments.append(" ".join(words[start_index:end_index]))

    return segments

def main(filename, num_threads):
    # Validate number of threads
    if num_threads < 1:
        print("Error: num_threads must be ≥ 1.")
        return

    # Try reading input file. Show errors if failed.
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Check for empty file
    if not text:
        print("Error: Input file is empty.")
        return

    # Divide text into segments for threading
    segments = divide_text(text, num_threads)

    # Prepare a list to hold each thread's result (Counter)
    result = [Counter() for _ in range(num_threads)]
    threads = []

    # Launch one thread per segment
    for i, seg in enumerate(segments):
        t = threading.Thread(target=count_words, args=(seg, result, i))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Consolidate intermediate Counters into the final count
    final_word_counts = Counter()
    for part in result:
        final_word_counts.update(part)

    # Display the final sorted word-frequency results
    print("\nFinal Word Frequency Count:")
    for word, freq in final_word_counts.most_common():
        print(f"{word}: {freq}")
    print("--- End of program ---")

if __name__ == "__main__":
    # Ensure correct command-line usage
    if len(sys.argv) != 3:
        print("Usage: python word_counter.py <filename> <thread>")
        sys.exit(1)

    # Run main with provided filename and thread/segment count
    main(sys.argv[1], int(sys.argv[2]))
