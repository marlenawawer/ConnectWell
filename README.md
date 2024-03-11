ConnectWell - Voice Assistant

Description: ConnectWell is a personal voice assistant created using the OpenAI API. The interface is built using Streamlit.

Usage Instructions:
To start using the app, slide the toggle to the right. Once the toggle is in the right position, you'll see the text "Recording started" at the bottom. Talk into the microphone while the recording is active.
To stop recording, simply slide the toggle to the left.

Installation
1. Clone the repository
   
1.1. Using SSH
git clone git@github.com:marlenawawer/ConnectWell.git

1.2. Using HTTPS
git clone https://github.com/marlenawawer/ConnectWell.git

3. Install libraies
pip install dotenv os halo openai speech_recognition pyttsx3 streamlit

4. Run the file
streamlit run ConnectWell.py
