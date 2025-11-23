package ca.keenan.beans;


import lombok.Data;

@Data
public class UserHealthData {
    // You can add more fields here to match your Angular form
    private int age;
    private double weight; // in kg
    private double height; // in cm
    private String smoker; // "yes" or "no"
    private int exerciseMinutes;
    private String dietRestrictions;
}