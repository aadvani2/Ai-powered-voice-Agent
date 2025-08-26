# AI-Powered Dental Voice Agent

A modern, AI-powered voice assistant designed specifically for dental practices to handle customer queries about appointments, insurance, and general dental services.
image.png
## 🌟 Features

### Voice Interface
- **Speech Recognition**: Hands-free interaction using your microphone
- **Text-to-Speech**: AI responses are spoken back to users
- **Real-time Processing**: Instant voice-to-text conversion

### AI-Powered Responses
- **Natural Language Processing**: Understands complex dental queries
- **Context-Aware**: Remembers conversation context
- **Professional Tone**: Dental-specific responses with medical accuracy

### Dental Practice Management
- **Appointment Scheduling**: Check availability and book appointments
- **Insurance Information**: Details about accepted insurance providers
- **Service Information**: Comprehensive list of dental services
- **Office Hours**: Real-time availability information

### User Experience
- **Modern UI**: Beautiful, responsive design with glassmorphism effects
- **Quick Actions**: Pre-defined buttons for common queries
- **Conversation History**: Track all interactions
- **Mobile Responsive**: Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Modern web browser with microphone access

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Ai-powered-voice-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📋 Usage

### Voice Interaction
1. Click the microphone button
2. Speak your question clearly
3. Wait for the AI response
4. The response will be spoken back to you

### Text Interaction
1. Type your question in the text input
2. Press Enter or click the send button
3. Receive AI response

### Quick Actions
Use the pre-defined buttons for common queries:
- **Office Hours**: Check practice operating hours
- **Insurance**: View accepted insurance providers
- **Services**: See available dental services
- **Book Appointment**: Schedule a new appointment

## 🏥 Dental Practice Customization

### Update Practice Information
Edit the `DENTAL_DATA` dictionary in `app.py`:

```python
DENTAL_DATA = {
    "practice_name": "Your Dental Practice Name",
    "address": "Your Practice Address",
    "phone": "Your Phone Number",
    "hours": {
        "Monday": "8:00 AM - 6:00 PM",
        # ... customize hours
    },
    "services": [
        "Your Service 1",
        "Your Service 2",
        # ... add your services
    ],
    "insurance": [
        "Insurance Provider 1",
        "Insurance Provider 2",
        # ... add accepted insurance
    ]
}
```

### Available Appointment Slots
Update the `AVAILABLE_SLOTS` list in `app.py` with your actual availability:

```python
AVAILABLE_SLOTS = [
    "Monday 9:00 AM", "Monday 10:00 AM",
    "Tuesday 9:00 AM", "Tuesday 10:00 AM",
    # ... add your available slots
]
```

## 🔧 Technical Details

### Architecture
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI**: OpenAI GPT-3.5-turbo
- **Speech**: Web Speech API
- **Styling**: Custom CSS with glassmorphism effects

### API Endpoints
- `GET /`: Main application interface
- `POST /api/process-voice`: Process voice/text queries
- `POST /api/speak`: Text-to-speech conversion
- `GET /api/appointment-slots`: Get available appointments
- `GET /api/insurance-info`: Get insurance information

### Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

**Note**: Speech recognition works best in Chrome-based browsers.

## 🛠️ Development

### Project Structure
```
Ai-powered-voice-Agent/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Stylesheets
    └── js/
        └── script.js     # JavaScript functionality
```

### Adding New Features
1. **New API Endpoints**: Add routes in `app.py`
2. **UI Components**: Modify `templates/index.html`
3. **Styling**: Update `static/css/style.css`
4. **Functionality**: Extend `static/js/script.js`

## 🔒 Security Considerations

- **API Key Protection**: Never commit your `.env` file
- **HTTPS**: Use HTTPS in production
- **Input Validation**: All user inputs are validated
- **Rate Limiting**: Consider implementing rate limiting for production

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up reverse proxy (Nginx, Apache)
4. Configure SSL certificates
5. Set up proper logging

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the browser console for error messages
- Ensure your OpenAI API key is valid
- Verify microphone permissions are granted

## 🔮 Future Enhancements

- [ ] Integration with dental practice management software
- [ ] Multi-language support
- [ ] Advanced appointment booking system
- [ ] Patient record integration
- [ ] Payment processing
- [ ] SMS/Email notifications
- [ ] Analytics dashboard
- [ ] Mobile app version

---

**Built with ❤️ for modern dental practices**
