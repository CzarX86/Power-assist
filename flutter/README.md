# Flutter Mobile App Setup Guide

## Overview

The Power Assist mobile app is built with Flutter and provides a native mobile experience for document processing.

## Features

- Upload documents from mobile device
- View document list with status indicators
- Process documents with agent tasks
- View document content and metadata
- Real-time status updates

## Prerequisites

- Flutter SDK 3.0.0 or higher
- Dart SDK
- Android Studio (for Android) or Xcode (for iOS)
- Running Power Assist API server

## Installation

1. Navigate to the Flutter project directory:
```bash
cd flutter/power_assist_mobile
```

2. Install dependencies:
```bash
flutter pub get
```

3. Configure the API endpoint in `lib/main.dart`:
```dart
ApiService(baseUrl: 'http://YOUR_SERVER_IP:8000')
```

## Running the App

### On Emulator/Simulator

```bash
flutter run
```

### On Physical Device

1. Enable developer mode on your device
2. Connect via USB
3. Run:
```bash
flutter run
```

### Build Release APK (Android)

```bash
flutter build apk --release
```

### Build Release IPA (iOS)

```bash
flutter build ios --release
```

## Project Structure

```
lib/
├── main.dart              # App entry point
├── services/
│   └── api_service.dart   # API communication
└── screens/
    └── home_screen.dart   # Main document list screen
```

## API Configuration

By default, the app connects to `http://localhost:8000`. For testing on physical devices:

1. Find your computer's IP address
2. Update the `baseUrl` in `main.dart`
3. Ensure the API server is accessible on your network

## Features Implementation Status

- [x] Document upload
- [x] Document list view
- [x] Status indicators
- [x] Pull to refresh
- [ ] Document detail view
- [ ] Agent task execution
- [ ] Content preview
- [ ] Offline support

## Customization

### Changing Theme

Edit `MaterialApp` theme in `main.dart`:

```dart
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  useMaterial3: true,
),
```

### Adding New Screens

1. Create new file in `lib/screens/`
2. Implement `StatefulWidget` or `StatelessWidget`
3. Add navigation in `home_screen.dart`

## Troubleshooting

### Cannot connect to API

- Ensure API server is running
- Check firewall settings
- Verify IP address and port
- For Android emulator, use `10.0.2.2` instead of `localhost`

### Build Issues

```bash
flutter clean
flutter pub get
flutter run
```

## Next Steps

- Implement document detail screen
- Add agent task execution UI
- Implement content preview
- Add offline caching
- Implement push notifications
