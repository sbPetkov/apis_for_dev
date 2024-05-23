import React from "react";
import { styles } from "./homeStyles.js";
import {
  View,
  Text,
  SafeAreaView,
  ImageBackground,
  ScrollView,
  Pressable,
} from "react-native";

import { Header } from "../../components/header.jsx";

import KITCHEN_SOURCE from "../../../assets/kitchen-pic.jpg";
import BATHROOM_SOURCE from "../../../assets/bathroom.jpg";
import TOILET_SOURCE from "../../../assets/toilet.png";

const Home = () => {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollViewContent}
        showsVerticalScrollIndicator={false}
      >
        <Header showProfilePic={true} />
        <View style={styles.text}>
          <Text style={styles.headerTitle}>Здравей, username!</Text>
          <Text style={styles.description}>
            За коя част от дома искаш да провериш потреблението си?
          </Text>
        </View>
        <Pressable
          style={styles.paddingZero}
          onPress={() => console.log("TODO: redirect")}
        >
          <ImageBackground style={styles.rooms} source={KITCHEN_SOURCE}>
            <Text style={styles.roomText}>Кухня</Text>
            <Text style={styles.devices}>5 уреда</Text>
          </ImageBackground>
        </Pressable>
        <Pressable
          style={styles.paddingZero}
          onPress={() => console.log("TODO: redirect")}
        >
          <ImageBackground style={styles.rooms} source={BATHROOM_SOURCE}>
            <Text style={styles.roomText}>Баня</Text>
            <Text style={styles.devices}>4 уреда</Text>
          </ImageBackground>
        </Pressable>
        <Pressable
          style={styles.paddingZero}
          onPress={() => console.log("TODO: redirect")}
        >
          <ImageBackground style={styles.rooms} source={TOILET_SOURCE}>
            <Text style={styles.roomText}>Тоалетна</Text>
            <Text style={styles.devices}>2 уреда</Text>
          </ImageBackground>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Home;
