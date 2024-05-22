import { View, Text, Image, StyleSheet } from "react-native";
import React from "react";
import { Tabs, Redirect } from "expo-router";
import getIcon from '../../utils/icons';





const TabIcon = ({localIcon, color, name, focused, iconName }) => {
  return (
    <View
      style={[{
        flexDirection: "row",
        alignItems: "center",
        // justifyContent: "center",
        // width: 100,
        gap: 10 
      }, focused ? {} : {}]}  // Here must find solution about the expanding on focus tab
    >
      {getIcon(iconName, color)}
      {/* <Image
        source={localIcon}
        style={{ resizeMode: "contain", height: 35, tintColor: color }}
      /> */}
      <Text style={[styles.tabIconText, {color: color}]}>
        {focused ? name : null}
      </Text>
    </View>
  );
};

const TabsLayout = () => {
  return (
    <Tabs
      screenOptions={{
        headerTransparent: true,
        tabBarShowLabel: false,
        tabBarStyle: styles.tabBar,
        tabBarItemStyle: styles.tabBarItem,
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="home/index"
        options={{
          title: "Home",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              color={color}
              name="Home"
              iconName={'home'}
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="tips/index"
        options={{
          title: "Tips",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // localIcon={require('../../assets/tabIcons/home.png')}
              color={color}
              name="Tips"
              iconName={'droplet'}
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="user/index"
        options={{
          title: "User",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // localIcon={require('../../assets/tabIcons/home.png')}
              color={color}
              iconName={'user'}
              name="User"
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="settings/index"
        options={{
          title: "Settings",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // localIcon={require('../../assets/tabIcons/home.png')}
              iconName={'settings'}
              color={color}
              name="Settings"
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="statistic/index"
        options={{
          title: "Statistics",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // localIcon={require('../../assets/tabIcons/home.png')}
              iconName={'bar-chart'}
              color={color}
              name="Statistics"
              focused={focused}
            />
        }}
      />
      <Tabs.Screen
        name="troubleshoot/index"
        options={{
          title: "Trouble",
          tabBarIcon: ({ color, focused }) =>
            <TabIcon
              // localIcon={require('../../assets/tabIcons/home.png')}
              iconName={'emergency-share'}
              color={color}
              name="Trouble"
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
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    // alignItems: "center",
    // justifyContent: "center",
    paddingLeft: 20,
    paddingRight: 20,
    borderTopWidth: 0,
    borderTopLeftRadius: 25,
    borderTopRightRadius: 25
  },
  tabBarItem: {
    flex: 1,
    display: "flex",
    // flexDirection: 'row',
    alignItems: "center",
    justifyContent: "center"
  },
  tabIconText: {
     fontSize: 15,
  }
});
