from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
from data.constants import AreasPage as AreasConstants

class AreasPage(BasePage):
    # Page Header Elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header span")
    NEW_AREA_BUTTON = (By.CSS_SELECTOR, "a[href='/admin/areas/new']")
    
    # Search and Filter Elements
    SEARCH_INPUT = (By.ID, "name")
    SORT_SELECT = (By.NAME, "order_by")
    STATUS_FILTER = (By.NAME, "status")
    ITEMS_PER_PAGE = (By.NAME, "count_per_page")
    
    # Table Elements
    TABLE = (By.CSS_SELECTOR, ".table")
    TABLE_HEADERS = (By.CSS_SELECTOR, "thead th")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    
    # Table Column Elements
    AREA_NAME = (By.CSS_SELECTOR, f"td:nth-child({AreasConstants.TableColumns.NAME})")
    SORT_ORDER = (By.CSS_SELECTOR, f"td:nth-child({AreasConstants.TableColumns.SORT_ORDER})")
    STATUS = (By.CSS_SELECTOR, f"td:nth-child({AreasConstants.TableColumns.STATUS}) .badge")
    ACTIONS = (By.CSS_SELECTOR, f"td:nth-child({AreasConstants.TableColumns.ACTION})")

    # Update column headers
    NAME_HEADER = (By.XPATH, f"//button[@data-button-type='{AreasConstants.TableColumns.NAME}']")
    SORT_ORDER_HEADER = (By.XPATH, f"//button[@data-button-type='{AreasConstants.TableColumns.SORT_ORDER}']")
    STATUS_HEADER = (By.XPATH, f"//button[@data-button-type='{AreasConstants.TableColumns.STATUS}']")

    EDIT_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Edit']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Delete']")
    
    # Pagination Elements
    PAGINATION = (By.CSS_SELECTOR, "nav.pagy.nav")
    NEXT_PAGE = (By.CSS_SELECTOR, "nav.pagy a[aria-label='Next']:not([aria-disabled='true'])")
    PREV_PAGE = (By.CSS_SELECTOR, "nav.pagy a[aria-label='Previous']:not([aria-disabled='true'])")
    CURRENT_PAGE = (By.CSS_SELECTOR, "nav.pagy a.current")
    PAGE_LINKS = (By.CSS_SELECTOR, "nav.pagy a:not([aria-label])")
    
    # Dropdown Locators
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".ts-wrapper.single")
    SORT_INPUT = (By.CSS_SELECTOR, ".ts-control")
    SORT_OPTIONS_LIST = (By.CSS_SELECTOR, ".ts-dropdown-content")
    SORT_OPTION = (By.CSS_SELECTOR, 'div[data-selectable][data-value="{}"]')

    STATUS_DROPDOWN = (By.CSS_SELECTOR, "[data-controller='admin--tom-select'][name='status']")
    STATUS_WRAPPER = (By.CSS_SELECTOR, "select[name='status'] ~ .ts-wrapper")
    STATUS_CONTROL = (By.CSS_SELECTOR, ".ts-control")
    STATUS_DROPDOWN_CONTENT = (By.CSS_SELECTOR, ".ts-dropdown-content")
    STATUS_OPTION = (By.CSS_SELECTOR, "div[data-value='{}']")
    STATUS_OPTIONS = {
        True: (By.CSS_SELECTOR, "div[data-value='true'].option"),
        False: (By.CSS_SELECTOR, "div[data-value='false'].option")
    }

    # Delete Modal Elements
    DELETE_MODAL = (By.ID, "modalDelete")
    MODAL_DIALOG = (By.CSS_SELECTOR, "#modalDelete .modal-dialog")
    DELETE_CONFIRM_TEXT = (By.CSS_SELECTOR, ".modal-body p")
    KEEP_RECORD_BUTTON = (By.CSS_SELECTOR, "button.btn--primary[data-bs-dismiss='modal']")
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--outline-danger[data-turbo-method='delete']")

    # No Records Locator
    NO_RECORDS = (By.CSS_SELECTOR, "td.text-danger.text-center[colspan='8']")

    # Error Alert Locator
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert.alert--danger .alert__content .col")

    def get_area_details(self, row):
        """Get details for an area row"""
        return {
            'name': row.find_element(*self.AREA_NAME).text,
            'sort_order': row.find_element(*self.SORT_ORDER).text,
            'status': row.find_element(*self.STATUS).text
        }

    def get_all_areas(self):
        """Get all areas from current page"""
        areas = []
        rows = self.find_elements(self.TABLE_ROWS)
        for row in rows:
            areas.append(self.get_area_details(row))
        return areas

    def search_area(self, name):
        """Search for an area by name"""
        try:
            self.logger.info(f"Searching for area: {name}")
            search_input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
            search_input.clear()
            search_input.send_keys(name)
            self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))
            return self
        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
            return self

    def sort_by(self, order):
        """Sort areas by given order"""
        try:
            self.logger.info(f"Sorting by: {order}")
            dropdown = self.wait.until(EC.presence_of_element_located(self.SORT_DROPDOWN))
            input_area = dropdown.find_element(*self.SORT_INPUT)
            self.driver.execute_script("arguments[0].click();", input_area)
            option_locator = (self.SORT_OPTION[0], self.SORT_OPTION[1].format(order))
            option = self.wait.until(EC.presence_of_element_located(option_locator))
            self.driver.execute_script("arguments[0].click();", option)
            self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))
            return self
        except Exception as e:
            self.logger.error(f"Failed to sort table: {str(e)}")
            return self

    def filter_by_status(self, status):
        """Filter areas by status"""
        try:
            self.logger.info(f"Filtering by status: {status}")
            wrapper = self.wait.until(EC.presence_of_element_located(self.STATUS_WRAPPER))
            control = wrapper.find_element(*self.STATUS_CONTROL)
            self.driver.execute_script("arguments[0].click();", control)
            option_locator = self.STATUS_OPTIONS[status]
            option = wrapper.find_element(*option_locator)
            self.driver.execute_script("arguments[0].click();", option)
            self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))
            return self
        except Exception as e:
            self.logger.error(f"Failed to filter by status: {str(e)}")
            return self

    def set_items_per_page(self, count):
        """Set number of items per page"""
        self.select_by_value(self.ITEMS_PER_PAGE, str(count))
        return self

    def click_new_area(self):
        """Click new area button and wait for navigation"""
        try:
            self.logger.info("Navigating to new area page")
            button = self.wait.until(EC.element_to_be_clickable(self.NEW_AREA_BUTTON))
            original_url = self.driver.current_url
            self.driver.execute_script("arguments[0].click();", button)
            self.wait.until(EC.url_changes(original_url))
            return self
        except Exception as e:
            self.logger.error(f"Failed to navigate to new area page: {str(e)}")
            return self

    def edit_area(self, name):
        """Edit area by name"""
        rows = self.find_elements(self.TABLE_ROWS)
        for row in rows:
            if row.find_element(*self.AREA_NAME).text == name:
                row.find_element(*self.EDIT_BUTTON).click()
                return True
        return False

    def delete_area(self, name):
        """Delete an area by name"""
        try:
            self.logger.info(f"Deleting area: {name}")
            rows = self.find_elements(self.TABLE_ROWS)
            for row in rows:
                if row.find_element(*self.AREA_NAME).text == name:
                    row.find_element(*self.DELETE_BUTTON).click()
                    self.wait.until(EC.presence_of_element_located(self.DELETE_MODAL))
                    confirm_button = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BUTTON))
                    confirm_button.click()
                    self.wait.until(EC.invisibility_of_element_located(self.DELETE_MODAL))
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete area: {str(e)}")
            return False

    def cancel_delete(self, name):
        """Cancel area deletion"""
        try:
            rows = self.find_elements(self.TABLE_ROWS)
            for row in rows:
                if row.find_element(*self.AREA_NAME).text == name:
                    row.find_element(*self.DELETE_BUTTON).click()
                    self.wait.until(EC.presence_of_element_located(self.DELETE_MODAL))
                    keep_button = self.wait.until(EC.element_to_be_clickable(self.KEEP_RECORD_BUTTON))
                    keep_button.click()
                    self.wait.until(EC.invisibility_of_element_located(self.DELETE_MODAL))
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to cancel delete: {str(e)}")
            return False

    def has_pagination(self):
        """Check if pagination is present"""
        try:
            pagination = self.find_element(self.PAGINATION)
            return pagination.is_displayed() and len(self.find_elements(self.PAGE_LINKS)) > 1
        except:
            return False

    def get_current_page_number(self):
        """Get current page number"""
        try:
            current = self.find_element(self.CURRENT_PAGE)
            return int(current.text)
        except:
            return 1

    def navigate_to_page(self, direction):
        """Navigate to next or previous page"""
        try:
            if direction == 'next':
                button = self.find_element(self.NEXT_PAGE)
            else:
                button = self.find_element(self.PREV_PAGE)
            self.driver.execute_script("arguments[0].click();", button)
            self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate {direction}: {str(e)}")
            return False

    def verify_no_records(self):
        """Verify no records found after search"""
        try:
            return self.wait.until(lambda d: 
                len(d.find_elements(*self.TABLE_ROWS)) == 0 or
                d.find_elements(*self.NO_RECORDS)[0].text.strip() == "No record found"
            )
        except Exception as e:
            self.logger.error(f"Failed to verify no records: {str(e)}")
            return False