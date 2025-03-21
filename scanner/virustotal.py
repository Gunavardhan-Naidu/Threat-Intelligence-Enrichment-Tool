import vt
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)


def vt_info(input_type:str,value: str) -> dict[str,any]:
    if not vt.Client:
        logging.error(f"VirusTotal API not configured")
    try:
        with vt.Client("") as client:

            #import base64 > url_id = base64.urlsafe_b64encode("http://www.somedomain.com/this/is/my/url".encode()).decode().strip("=")
            if input_type == "url":
                url_id = vt.url_id(value)
                output = client.get_object(f"/urls/{url_id}")
                # logging.info(f"Processing your URL: {url_id}")
            elif input_type == "domain":
                output = client.get_object(f"/domains/{value}")
                # logging.info(f"Processing your domain: {value}")
            elif input_type == "ipaddress":
                output = client.get_object(f"/ip_addresses/{value}")
                # logging.info(f"Processing your ipaddress: {value}")
            else:
                error_msg = f"Unsupported input type for VirusTotal: {input_type}"
                logging.error(error_msg)
                return {"error": error_msg}
            
            vt_data = {
                    "last_analysis_stats": output.last_analysis_stats,
                    "reputation": getattr(output, "reputation", None),
                    "categories": getattr(output, "categories", []),
                    "last_modification_date": getattr(output, "last_modification_date", None)
                }
            return vt_data
    except Exception as e:
        logging.error(f"VirusTotal lookup failed for {value}: {str(e)}")
        return {"error": str(e)}
    
# if client:
#         client.close()
        

        
