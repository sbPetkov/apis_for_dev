import { StyleSheet } from "react-native";

const CARD_HEIGHT = 170;

export const styles = StyleSheet.create({
  container: {
    width: "88%",
    flex: 1,
    flexDirection: "column",
    gap: 3,
    marginHorizontal: 24,
    marginVertical: 35,
  },
  scrollViewContent: {
    flexGrow: 1,
  },
  headerTitle: {
    fontSize: 25,
    paddingBottom: 15,
  },
  description: {
    fontSize: 15,
    color: "grey",
    letterSpacing: 0.1,
    lineHeight: 25,
  },
  paddingZero: {
    padding: 0,
  },
  text: {
    marginVertical: 35,
    fontStyle: "normal",
  },
  rooms: {
    height: CARD_HEIGHT,
    justifyContent: "flex-end",
    borderRadius: 20,
    overflow: "hidden",
    marginVertical: 10,
    paddingLeft: 24,
    paddingRight: 24,
    paddingTop: 20,
    paddingBottom: 20,
  },
  roomText: {
    color: "white",
    fontSize: 25,
    fontWeight: "bold",
    marginBottom: 8,
    fontStyle: "bolder",
  },
  devices: {
    color: "white",
    fontSize: 18,
    fontWeight: "bold",

    fontStyle: "bolder",
  },
});
