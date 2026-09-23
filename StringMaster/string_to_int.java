class Solution {
    public int myAtoi(String s) {
        int i = 0;

        // Ignore leading whitespaces
        while (i < s.length() && s.charAt(i) == ' ') { i++; }

        int sign = 1;

        // Check for the sign
        if (i < s.length() && (s.charAt(i) == '+' || s.charAt(i) == '-')) {
            sign = (s.charAt(i) == '-') ? -1 : 1;
            i++;
        }

        int result = 0;

        // Convert remaining digits to integer
        while (i < s.length() && Character.isDigit(s.charAt(i))) {
            int digit = s.charAt(i) - '0';  // Convert to integer by ASCII subtraction

            // Handle overflow and underflow (MAX: 2^31 - 1 | MIN: 2^31)
            if (result > (Integer.MAX_VALUE - digit) / 10) { return (sign == 1) ? Integer.MAX_VALUE : Integer.MIN_VALUE; }
            
            // Shift the previous value one decimal to left and continue
            result = result * 10 + digit;
            i++;
        }

        // Apply the sign
        return result * sign;
    }
}
