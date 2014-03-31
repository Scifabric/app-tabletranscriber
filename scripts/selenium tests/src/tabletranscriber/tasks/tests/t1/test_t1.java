package tabletranscriber.tasks.tests.t1;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

import tabletranscriber.tasks.tests.util.Util;

public class test_t1 {
	private final int NUMBER_OF_TASK_RUNS_T1_BY_USER = 25;
	private StringBuffer verificationErrors = new StringBuffer();
	private String baseUrl = "http://localhost";
	private WebDriver driver;
	
	@Before
	public void setUp() throws Exception {
		// FirefoxProfile firefoxProfile = new FirefoxProfile();
		// firefoxProfile.addExtension(file);
		// firefoxProfile.setPreference("extensions.firebug.currentVersion",
		// "1.8.1"); // Avoid startup screen
		//
		// File f = new File("/home/guilhermeg/browsers/firefox/firefox-bin");
		// FirefoxBinary fbin = new FirefoxBinary(f);

		// driver = new FirefoxDriver(fbin, firefoxProfile);

		driver = new FirefoxDriver();
		driver.manage().window().setSize(new Dimension(1200, 700));
		driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	}

	@Test
	public void testTest_t1_aaa() throws Exception {
		Util.login(driver, baseUrl, "aaa@gmail.com", "aaa");
		
		driver.get(baseUrl
				+ "/pybossa/app/caracterizaoeten2001bras_tt1/newtask");
		
		for (int i = 0; i < NUMBER_OF_TASK_RUNS_T1_BY_USER; i++) {
			assertEquals(
					"Socientize · Application: Caracterização e tendências da rede urbana do Brasil: configurações atuais e tendências da rede urbana (Vol. I; 2001) Seleção · Contribute",
					driver.getTitle());
			driver.findElement(By.id("button_yes")).click();
		}

		driver.close();
	}

	@Test
	 public void testTest_t1_bbb() throws Exception {
		 Util.login(driver, baseUrl, "bbb@gmail.com", "bbb");
		
		 driver.get(baseUrl
		 + "/pybossa/app/caracterizaoeten2001bras_tt1/newtask");
		 
		 for (int i = 0; i < NUMBER_OF_TASK_RUNS_T1_BY_USER; i++) {
			 assertEquals("Socientize · Application: Caracterização e tendências da rede urbana do Brasil: configurações atuais e tendências da rede urbana (Vol. I; 2001) Seleção · Contribute",
					 driver.getTitle());
			 driver.findElement(By.id("button_yes")).click();
		 }
		
		 driver.close();
	 }

	// @Test
	// public void testTest_t1_ccc() throws Exception {
	// selenium.open("/pybossa/account/signin");
	// selenium.type("email", "ccc@gmail.com");
	// selenium.type("password", "ccc");
	// selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
	// selenium.waitForPageToLoad("30000");
	//
	// selenium.open("/pybossa/app/anuario1916pb_tt1/newtask");
	// // selenium.open("/pybossa/app/caracterizaoeten2001bras_tt1/newtask");
	//
	// for (int i = 0; i < NUMBER_OF_TASKS_T1_BY_USER; i++) {
	// selenium.click("button_yes");
	// //
	// assertEquals("PyBossa · Application: Annuario Estatistico da Parahyba do Norte 1916 Seleção · Contribute",
	// // selenium.getTitle());
	// //
	// assertEquals("PyBossa · Application: Caracterização e tendências da rede urbana do Brasil: configurações atuais e tendências da rede urbana Seleção · Contribute",
	// // selenium.getTitle());
	// }
	//
	// selenium.close();
	// }

	@After
	public void tearDown() throws Exception {
		driver.quit();
		String verificationErrorString = verificationErrors.toString();
		if (!"".equals(verificationErrorString)) {
			fail(verificationErrorString);
		}
	}
}
