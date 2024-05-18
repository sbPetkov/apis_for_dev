import { View, Text, Image } from 'react-native';
import React from 'react';
import { Tabs, Redirect } from 'expo-router';
import { StyleSheet } from 'react-native';

const TabIcon = ({icon, color, name, focused}) => {
  return(
    <View>
      <Image 
      source={icon}
      resizeMode='contain'
      tintColor={color}
    //   className="w-6 h-6"
      />
    </View>
  )
}

const TabsLayout = () => {
  return (
    <>
    <Tabs screenOptions={{
        tabBarStyle: styles.tabBar,
        tabBarItemStyle: styles.tabBarItem,
        headerShown: false,
      }}>
      <Tabs.Screen 
        name='home' style={styles.itemColor}
        options={{
            tabBarLabel: 'Home',
            tabBarIcon: ({ color, focused }) => (
              <TabIcon
                // icon={require('./path/to/home-icon.png')}
                color={color}
                focused={focused}
              />
            ),
          }}
          />
      <Tabs.Screen 
        name='list' style={styles.itemColor}
        options={{
            tabBarLabel: 'List',
            tabBarIcon: ({ color, focused }) => (
              <TabIcon
                // icon={require('./path/to/home-icon.png')}
                color={color}
                focused={focused}
              />
            ),
          }}
          />
    </Tabs>
    </>
  )
}



export default TabsLayout;

const styles = StyleSheet.create({
  tabBar: {
    display: 'flex',
    // backgroundColor: 'black',
    // justifyContent: 'space-between',
    borderTopWidth: 0, // Adjust thickness
    borderTopLeftRadius: 25,
    borderTopRightRadius: 25,
    // borderTopColor: '#000', // Change to desired color
  },
  tabBarItem: {
    // borderRightWidth: 1, // Add border to the right of each tab
    borderRightColor: '#ccc', // Change to desired color
  },
});