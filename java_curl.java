// Basic java script for testing SSL handhake errors.
// javac java_curl.java && java httpCall <optional_url>

import java.net.URL;
import java.net.HttpURLConnection;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;


class httpCall {
    public static void main(String args[]) throws IOException {

        String url_string;

        // curl_init and url
        if (args.length > 0) {
            System.out.println("Args:" + args[0]);
            url_string = args[0];
        } else {
            url_string = "https://www.apple.com";
        }
        System.out.println(url_string);
        URL url = new URL(url_string);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();

        //  CURLOPT_POST
        con.setRequestMethod("POST");

        // CURLOPT_FOLLOWLOCATION
        con.setInstanceFollowRedirects(true);

        String postData = "my_data_for_posting";
        con.setRequestProperty("Content-length", String.valueOf(postData.length()));

        con.setDoOutput(true);
        con.setDoInput(true);

        DataOutputStream output = new DataOutputStream(con.getOutputStream());
        output.writeBytes(postData);
        output.close();

        // "Post data send ... waiting for reply");
        int code = con.getResponseCode(); // 200 = HTTP_OK
        System.out.println("Response    (Code):" + code);
        System.out.println("Response (Message):" + con.getResponseMessage());

        // read the response
        DataInputStream input = new DataInputStream(con.getInputStream());
        int c;
        StringBuilder resultBuf = new StringBuilder();
        while ( (c = input.read()) != -1) {
            resultBuf.append((char) c);
        }
        input.close();

        System.out.println(resultBuf.toString());
    }
}
