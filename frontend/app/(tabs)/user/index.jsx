import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const User = () => {
  return (
    <View style={styles.container}>
      <Text>Welcome to the User Screen!</Text>
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

export default User;