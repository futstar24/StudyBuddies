import React from 'react';
import { View, StyleSheet, Platform } from 'react-native';
import { WebView as RNWebView } from 'react-native-webview';


const DEV_URL = "https://e14062411cbd.ngrok-free.app"; 
const PROD_URL = "";  

export default function Index() {
  const uri = process.env.NODE_ENV === "development" ? DEV_URL : PROD_URL;

  if (Platform.OS === 'web') {
    return (
      <View style={styles.container}>
        <iframe
          src={uri}
          style={{ border: 0, width: '100%', height: '100%' }}
          allow="clipboard-read; clipboard-write; fullscreen"
        />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <RNWebView
        source={{ uri }}
        style={{ flex: 1 }}
        sharedCookiesEnabled={true}
        thirdPartyCookiesEnabled={true}
      />
    </View>
  );

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
