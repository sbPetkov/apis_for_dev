import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const Troubleshoot = () => {
  return (
    <View style={styles.container}>
      <Text>Welcome to the Troubleshoot Screen!</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default Troubleshoot;