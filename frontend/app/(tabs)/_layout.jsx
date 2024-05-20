import { View, Text, Image } from "react-native";
import React from "react";
import { Tabs, Redirect } from "expo-router";
import { StyleSheet } from "react-native";

const TabIcon = ({ icon, color, name, focused }) => {
  return (
    <View
      style={{
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: 2
      }}
    >
      <Image
        source={icon}
        style={{ resizeMode: "contain", height: 35, tintColor: color }}
      />
      <Text style={{ color: color, fontSize: 18 }}>
        {focused ? name : null}
      </Text>
    </View>
  );
};

const TabsLayout = () => {
  return (
    <Tabs
      screenOptions={{
        tabBarShowLabel: false,
        tabBarStyle: styles.tabBar,
        tabBarItemStyle: styles.tabBarItem,
        headerShown: false
      }}
    >
      <Tabs.Screen
        name="home"
        options={{
          title: "Home",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              icon={require("../../assets/tabIcons/home.png")}
              color={color}
              name="Home"
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="list"
        options={{
          title: "List",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // icon={require('../../assets/tabIcons/list.png')}
              color={color}
              name="List"
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // icon={require('../../assets/tabIcons/profile.png')}
              color={color}
              name="Profile"
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: "Settings",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // icon={require('../../assets/tabIcons/settings.png')}
              color={color}
              name="Settings"
              focused={focused}
            />
        }}
      />
    </Tabs>
  );
};

export default TabsLayout;

const styles = StyleSheet.create({
  tabBar: {
    display: "flex",
    // flexDirection: 'row',
    alignItems: "center",
    justifyContent: "center",
    paddingLeft: 20,
    paddingRight: 20,
    borderTopWidth: 0,
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30
  },
  tabBarItem: {
    flex: 1,
    display: "flex",
    // flexDirection: 'row',
    alignItems: "center",
    justifyContent: "center"
  }
  // tabBarLabel: {
  //   fontSize: 20,
  //   fontWeight: 'bold',
  // },
});
