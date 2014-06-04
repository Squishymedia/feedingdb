from selenium import selenium
from basecase import BaseTestCase
import unittest, time, re


class TestDataentry(BaseTestCase):
    def test_data_entry(self):
        sel = self.selenium
        sel.open("/admin/")
        sel.click("link=Login")
        sel.wait_for_page_to_load("30000")
        sel.type("id_username", "xxxxx")
        sel.type("id_password", "xxxx")
        sel.click("//input[@value='Log in']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Please enter a correct username and password. Note that both fields are case-sensitive."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_username", "xianhua")
        sel.type("id_password", "12345")
        sel.click("//input[@value='Log in']")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Add")
        sel.wait_for_page_to_load("30000")
        sel.type("id_title", "Xianhua Test Study")
        sel.click("//img[@alt='Calendar']")
        sel.click("link=18")
        sel.type("id_description", "This is a test")
        sel.type("id_studyprivate_set-0-pi", "Xianhua")
        sel.click("_save")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("The study \"Xianhua Test Study\" was added successfully."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("searchbar", "Xianhua Test Study")
        sel.click("//input[@value='Search']")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='changelist']/form/table/tbody/tr[2]/td[6]/a[1]/img")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Subjects")
        sel.click("link=Add subject")
        sel.wait_for_page_to_load("30000")
        sel.select("id_taxon", "label=Didelphis virginianus")
        sel.type("id_name", "test subject didelphis")
        sel.type("id_illustration_set-0-picture", "/Users/xianhua/Pictures/feeding_logo.jpg")
        sel.click("_save")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("The subject \"test subject didelphis\" was added successfully."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Experiments")
        sel.click("link=Subjects")
        try: self.failUnless(sel.is_text_present("test subject didelphis"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Experiments")
        sel.click("link=Add experiment")
        sel.wait_for_page_to_load("30000")
        sel.click("technique_emg")
        sel.type("id_title", "Test Experiment Selenium")
        sel.select("id_subject", "label=test subject didelphis")
        sel.type("id_description", "Test description")
        sel.select("id_subj_devstage", "label=Adult")
        sel.type("id_illustration_set-0-picture", "/Users/xianhua/Pictures/feeding_logo.jpg")
        sel.type("id_illustration_set-0-notes", "Experiment picture")
        sel.click("_save")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("The experiment \"Test Experiment Selenium\" was added successfully."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Experiments")
        sel.click("//div[@id='pages']/div[3]/div/div/div/fieldset/table[1]/tbody/tr/td[7]/a[2]/img")
        sel.wait_for_page_to_load("30000")
        sel.click("link=EMG")
        sel.wait_for_page_to_load("30000")
        sel.type("id_illustration_set-0-picture", "/Users/xianhua/Pictures/feeding_logo.jpg")
        sel.type("id_illustration_set-0-notes", "EMG picture")
        sel.type("id_emgsensor_set-0-name", "EMG 1")
        sel.select("id_emgsensor_set-0-location_controlled", "label=Cricothyroid")
        sel.select("id_emgsensor_set-0-loc_side", "label=Left")
        sel.select("id_emgsensor_set-0-loc_ap", "label=Anterior")
        sel.select("id_emgsensor_set-0-loc_dv", "label=Dorsal")
        sel.select("id_emgsensor_set-0-loc_pd", "label=Proximal")
        sel.select("id_emgsensor_set-0-loc_ml", "label=Medial")
        sel.select("id_emgsensor_set-0-axisdepth", "label=Superficial")
        sel.select("id_emgsensor_set-0-unit", "label=millivolt")
        sel.select("id_emgsensor_set-0-emg_filtering", "label=60Hz notch")
        sel.type("id_emgsensor_set-0-emg_amplification", "12")
        sel.click("_save")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("The EMG setup \"EMG setup with preamplifier: \" was changed successfully."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Sessions")
        sel.wait_for_page_to_load("30000")
        sel.type("id_session_set-0-accession", "1")
        sel.type("id_session_set-0-title", "test session 1")
        sel.type("id_session_set-0-bookkeeping", "1")
        sel.type("id_session_set-0-position", "1")
        sel.select("id_session_set-0-subj_restraint", "label=Box")
        sel.type("id_session_set-0-subj_anesthesia_sedation", "test")
        sel.click("_save")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Successfully updated the data!"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=View")
        sel.wait_for_page_to_load("30000")
        sel.click("//img[@alt='view']")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Channel Lineup")
        sel.click("link=Edit")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Channel Lineup")
        sel.type("id_channellineup_set-0-position", "1")
        sel.select("id_channellineup_set-0-channel", "label=EMG 1")
        sel.click("//div[@id='pages']/div[2]/div/div[2]/input")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Channel Lineup")
        sel.type("id_channellineup_set-1-position", "2")
        sel.click("//div[@id='pages']/div[2]/div/div[2]/input")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Channel Lineup")
        sel.click("link=Trials")
        sel.type("id_trial_set-0-title", "test trial")
        sel.type("id_trial_set-0-position", "1")
        sel.type("id_trial_set-0-estimated_duration", "12")
        sel.type("id_trial_set-0-food_type", "cookie")
        sel.type("id_trial_set-0-food_size", "12")
        sel.type("id_trial_set-0-food_property", "soft")
        sel.select("id_trial_set-0-behavior_primary", "label=Suckling")
        sel.type("id_trial_set-0-data_file", "/Users/xianhua/Pictures/feeding_logo.jpg")
        sel.click("//div[@id='pages']/div[3]/div/div[2]/input")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("The session \"test session 1\" was changed successfully."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Trials")
        sel.click("link=Mine")
        sel.wait_for_page_to_load("30000")
        sel.type("searchbar", "Xianhua Test Study")
        sel.click("//input[@value='Search']")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='changelist']/form/table/tbody/tr[2]/td[6]/a[3]/img")
        sel.wait_for_page_to_load("30000")
        sel.click("//input[@value=\"Yes, I'm sure\"]")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("The study \"Xianhua Test Study\" was deleted successfully."))
        except AssertionError, e: self.verificationErrors.append(str(e))

if __name__ == "__main__":
    unittest.main()