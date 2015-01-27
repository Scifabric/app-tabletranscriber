package com.example.tests;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

import java.io.File;
import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.NoAlertPresentException;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxBinary;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;

import com.thoughtworks.selenium.webdriven.WebDriverBackedSelenium;

public class Test1 {
  private WebDriver driver;
  private String baseUrl;
  private boolean acceptNextAlert = true;
  private StringBuffer verificationErrors = new StringBuffer();
  private com.thoughtworks.selenium.webdriven.WebDriverBackedSelenium selenium;

  @Before
  public void setUp() throws Exception {
	  File file = new File("/home/guilhermeg/browsers/firebug-1.8.1.xpi");
	  FirefoxProfile firefoxProfile = new FirefoxProfile();
	  firefoxProfile.addExtension(file);
	  firefoxProfile.setPreference("extensions.firebug.currentVersion", "1.8.1"); // Avoid startup screen
	  
	  File f = new File("/home/guilhermeg/browsers/firefox/firefox-bin");
	  FirefoxBinary fbin = new FirefoxBinary(f);
	  
	  baseUrl = "http://localhost";

	  driver = new FirefoxDriver(fbin, firefoxProfile);
	  
	  driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	  
	  selenium = new WebDriverBackedSelenium(driver, baseUrl);
  }

  @Test
  public void test1() throws Exception {
    selenium.open("/pybossa/api");
    String text = selenium.getBodyText();
    assertEquals(text, "The PyBossa API");
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

  private boolean isElementPresent(By by) {
    try {
      driver.findElement(by);
      return true;
    } catch (NoSuchElementException e) {
      return false;
    }
  }

  private boolean isAlertPresent() {
    try {
      driver.switchTo().alert();
      return true;
    } catch (NoAlertPresentException e) {
      return false;
    }
  }

  private String closeAlertAndGetItsText() {
    try {
      Alert alert = driver.switchTo().alert();
      String alertText = alert.getText();
      if (acceptNextAlert) {
        alert.accept();
      } else {
        alert.dismiss();
      }
      return alertText;
    } finally {
      acceptNextAlert = true;
    }
  }
}
