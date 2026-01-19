"""
Example application-specific page automation handlers.
This file serves as a template for creating your own `app_handlers.py`.
Copy this file to `app_handlers.py` and implement the specific automation
logic for your application. `app_handlers.py` is ignored by Git.
"""
from selenium.webdriver.common.by import By
from browser_automation import WebDriverManager
from config_models import AutomationConfig
import logging


# Setup logger for this module
logger = logging.getLogger("example_app_handlers")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.handlers = [handler]


class BasePageHandler:
    """Base class for page handlers."""

    def __init__(self, driver_manager: WebDriverManager, config: AutomationConfig):
        self.driver_manager = driver_manager
        self.config = config

    def setup_window_layout(self, x: int, y: int, width: int, height: int):
        """Setup window position and size for this page."""
        self.driver_manager.set_window_position_and_size(x, y, width, height)


class Page1Handler(BasePageHandler):
    """Handles automation for the SCADA alarms page."""

    def navigate_and_setup(self):
        """Navigate to alarms page and perform initial setup."""
        logger.info("Navigating to Page 1...")
        self.driver_manager.navigate_to(self.config.urls.page1_url)
        # TODO: Implement page-specific setup logic here
        # self._close_menu()
        # self._configure_alarm_filters()
        self._resize_table_headers()
        self._setup_page1_window_layout()

    def _resize_table_headers(self):
        """
        Resize table headers and body cells using JavaScript.
        Features:
        - Persistent MutationObserver to handle app re-renders.
        - Support for manual resizing by detecting user interaction.
        - "Learns" new widths when user resizes manually.
        """
        try:
            script = """
                // 1. Initialize Configuration (Persistent across re-runs)
                if (!window.iaColumnConfig) {
                    window.iaColumnConfig = {
                        'select': '50px',
                        'activeTime': '250px',
                        'Alternate Language': '750px',
                        'priority': '100px'
                    };
                }
                
                // Flag to track if user is currently resizing
                if (typeof window.iaIsResizing === 'undefined') {
                    window.iaIsResizing = false;
                }

                // 2. Event Listeners for Manual Resizing
                // We use global listeners with delegation to handle dynamic elements
                if (!window.iaResizeHandlersAttached) {
                    document.addEventListener('mousedown', function(e) {
                        if (e.target && e.target.classList.contains('thc-resize-handle')) {
                            window.iaIsResizing = true;
                            // console.log("User started resizing");
                        }
                    }, true);

                    document.addEventListener('mouseup', function(e) {
                        if (window.iaIsResizing) {
                            window.iaIsResizing = false;
                            // console.log("User finished resizing");
                            // Force a sync to lock in the new values
                            applyColumnStyles();
                        }
                    }, true);
                    window.iaResizeHandlersAttached = true;
                }

                // 3. Main Logic: Apply or Learn Styles
                function applyColumnStyles() {
                    const cells = document.querySelectorAll('.ia_table__cell');
                    let count = 0;

                    // A. If User IS Resizing: LEARN new widths from DOM
                    if (window.iaIsResizing) {
                        cells.forEach(cell => {
                            // Only look at headers to get the 'truth'
                            if (cell.classList.contains('ia_table__head__header__cell')) {
                                const colId = cell.getAttribute('data-column-id');
                                const currentWidth = cell.style.width;
                                
                                // Update config if logic exists and we have a valid width
                                if (colId && window.iaColumnConfig[colId] && currentWidth) {
                                    window.iaColumnConfig[colId] = currentWidth;
                                }
                            }
                        });
                        return 0; // Don't enforce styles while dragging
                    }

                    // B. If User NOT Resizing: ENFORCE widths from Config
                    cells.forEach(cell => {
                        const colId = cell.getAttribute('data-column-id');
                        if (colId && window.iaColumnConfig[colId]) {
                            const desiredWidth = window.iaColumnConfig[colId];
                            
                            // Check if enforcement is needed (avoid expensive DOM writes)
                            // We use !important to prevent the app from reverting styles randomly
                            if (cell.style.width !== desiredWidth) {
                                cell.style.setProperty('width', desiredWidth, 'important');
                                cell.style.setProperty('min-width', desiredWidth, 'important');
                                cell.style.setProperty('max-width', desiredWidth, 'important');
                                cell.style.setProperty('flex', '0 0 ' + desiredWidth, 'important');
                                cell.style.setProperty('box-sizing', 'border-box', 'important');
                                cell.style.setProperty('overflow', 'hidden', 'important');
                                count++;
                            }
                        }
                    });
                    return count;
                }

                // 4. Run immediately
                const initialCount = applyColumnStyles();

                // 5. Setup Observer to persist styles
                if (!window.iaTableResizeObserver) {
                    window.iaTableResizeObserver = new MutationObserver((mutations) => {
                        applyColumnStyles();
                    });
                    
                    window.iaTableResizeObserver.observe(document.body, { 
                        childList: true, 
                        subtree: true,
                        attributes: true, // Watch for style changes too
                        attributeFilter: ['style', 'class'] 
                    });
                }
                
                return initialCount;
            """
            count = self.driver_manager.driver.execute_script(script)
            logger.info(f"Initialized smart table resizing setup.")
        except Exception as e:
            logger.warning(f"Could not resize table headers: {e}")

    def _close_menu(self):
        """(Example) Close the navigation menu."""
        logger.info("Example: Closing menu (not implemented).")

    def _configure_alarm_filters(self):
        """(Example) Open config popup and apply filters."""
        logger.info("Example: Configuring alarm filters (not implemented).")

    def _set_priority_filters(self):
        """(Example) Set minimum and maximum priority filters."""
        logger.info("Example: Setting priority filters (not implemented).")

    def _set_category_filters(self):
        """(Example) Set category filters."""
        logger.info("Example: Setting category filters (not implemented).")

    def _hide_filters_panel(self):
        """(Example) Hide the filters panel."""
        logger.info("Example: Hiding filters panel (not implemented).")

    def _setup_page1_window_layout(self):
        """Setup window layout for alarms page."""
        import pyautogui
        screen_width, screen_height = pyautogui.size()
        y_position = (self.config.window.app_window_height - self.config.window.app_window_header_height - self.config.window.page1_header_height)

        # Calculate height based on configured total app height to prevent multi-monitor overflow
        bottom_limit = self.config.window.app_window_height
        height = bottom_limit - y_position

        self.setup_window_layout(self.config.window.window_x_offset, y_position, screen_width, height)


class Page2Handler(BasePageHandler):
    """Handles automation for the SCADA overview page."""

    def navigate_and_setup(self):
        """Navigate to overview page and perform initial setup."""
        logger.info("Navigating to Page 2...")
        self.driver_manager.navigate_to(self.config.urls.page2_url)
        # TODO: Implement page-specific setup logic here
        self._setup_page2_window_layout()

    def _setup_page2_window_layout(self):
        """Setup window layout for overview page."""
        import pyautogui
        screen_width, _ = pyautogui.size()
        self.setup_window_layout(
            self.config.window.window_x_offset,
            -self.config.window.app_window_header_height,
            screen_width,
            self.config.window.app_window_height
        )
