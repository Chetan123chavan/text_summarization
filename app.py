from flask import Flask, render_template, request, redirect, url_for
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/back', methods=['POST'])
def go_back():
    return redirect(url_for('text_summarization'))

@app.route('/text_summarization', methods=['GET', 'POST'])
def text_summarization():
    if request.method == 'POST':
        text = request.form['text']
        summarized_text = summarize_text(text)
        return render_template('text_summarization_result.html', summarized_text=summarized_text)
    return render_template('text_summarization.html')

@app.route('/youtube_transcript_summarization', methods=['GET', 'POST'])
def youtube_transcript_summarization():
    if request.method == 'POST':
        youtube_link = request.form['youtube_link']
        summarized_text = summarize_youtube_transcript(youtube_link)
        return render_template('youtube_transcript_summary.html', summarized_text=summarized_text)
    return render_template('youtube_transcript_summarization.html')

def summarize_text(text):
    summarizer = pipeline("summarization")
    summarized_text = summarizer(text, max_length=300, clean_up_tokenization_spaces=True)[0]['summary_text']
    return summarized_text

def summarize_youtube_transcript(youtube_link):
    
    video_id = youtube_link.split('?v=')[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ' '.join([line['text'] for line in transcript])
    summarized_text = summarize_text(transcript_text)
    return summarized_text

if __name__ == '__main__':
    app.run(debug=True)