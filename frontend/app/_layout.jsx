import { StatusBar } from 'expo-status-bar';
import { Text, View, StyleSheet } from 'react-native';
import {Link , Redirect, Stack} from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

const StackLayout =()=> {
  return (
    <SafeAreaProvider>
      <Stack>
        <Stack.Screen name="(tabs)" />
      </Stack>
    </SafeAreaProvider>
  );
}

// const styles = StyleSheet.create({
//   safeArea: {
//     flex: 1,
//   },
// });