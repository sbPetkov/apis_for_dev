import { StatusBar } from 'expo-status-bar';
import { Text, View, StyleSheet } from 'react-native';
import {Link , Redirect, Stack} from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

const StackLayout =()=> {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" />
    </Stack>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
});