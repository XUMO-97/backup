/* *****************************************************************************
 *  Name:    Tim Feng
 *  University: Princeton 2021
 *  Email:   tzfeng@princeton.edu
 *
 *  Description: Java implementation of coding puzzle for Onchain software
 *  summer position.
 **************************************************************************** */

import java.util.Hashtable;
import java.util.LinkedList;
import java.util.Scanner;

public class Onchain {

    private int first; // amount of product purchased by first customer
    private int n; // total number of product purchases
    private final double p; // price of the product
    private LinkedList<String> customers; // record of names of customers
    private Hashtable<String, Pair> ledger; // tracks amount purchased, dividend

    // helper class that contains product purchase and dividend information
    private class Pair {
        private int amount; // stores total products purchased by customer
        private double dividend; // stores total dividend of customer

        // constructor that takes amount and dividend as arguments
        public Pair(int amount, double dividend) {
            this.amount = amount;
            this.dividend = dividend;
        }

        // returns total products purchased by customer
        private int getAmount() {
            return amount;
        }

        // returns total dividend of customer
        private double getDividend() {
            return dividend;
        }

        // modifies total products purchased by customer after additional purchase
        private void setAmount(int products) {
            this.amount = products;
        }

        // modifies total dividend of customer after distribution or withdrawal
        private void setDividend(double change) {
            this.dividend = change;
        }
    }

    // constructor for data type that handles purchases of product at any price
    public Onchain(double price) {
        first = 0;
        n = 0;
        p = price;
        customers = new LinkedList<>();
        ledger = new Hashtable<>();
    }

    // distributes money to company and dividends to customers after a purchase
    public void purchase(String name, int quantity) {
        Pair purchase;
        // case 1: no dividends need to be distributed after first customer.
        if (customers.isEmpty()) {
            purchase = new Pair(quantity, 0.0);
            ledger.put(name, purchase);
            customers.add(name);
            first = quantity;
            n = quantity;
        }
        // case 2: more than one customer and dividends need to be distributed
        else {
            // case for new customer
            if (!customers.contains(name)) purchase = new Pair(quantity, 0.0);
                // case for repeat customer
            else {
                purchase = ledger.get(name);
                purchase.setAmount(purchase.getAmount() + quantity);
            }
            ledger.put(name, purchase);
            // distribute dividend across all customers before the current one
            for (String customer : customers) {
                Pair current = ledger.get(customer);
                current.setDividend(current.getDividend() +
                        ((double) current.getAmount() / n) * quantity * p / 2);
                ledger.put(customer, current);
            }
            // only add customer name if he/she is a first-time customer
            if (!customers.contains(name)) customers.add(name);
            n += quantity;
        }
    }

    // allows a customer to withdraw dividend and calculates remaining dividend
    public void withdraw(String name, double amount) {
        Pair balance = ledger.get(name);
        // check that amount withdrawn does not exceed remaining dividend
        if (balance.getDividend() < amount) throw new IllegalArgumentException
                ("Customer " + name + " has over-drafted and the withdrawal has " +
                        "been cancelled");
        balance.setDividend(balance.getDividend() - amount);
        ledger.put(name, balance);

    }

    // allows a customer to check his/her current dividend balance
    public double balance(String name) {
        // only carry out operation if the argument is a name of existing customer
        if (!customers.contains(name)) throw new IllegalArgumentException(
                "Invalid customer name");
        return ledger.get(name).getDividend();
    }

    // allows a customer to check how many product he/she has purchased
    public int inventory(String name) {
        // only carry out operation if the argument is a name of existing customer
        if (!customers.contains(name)) throw new IllegalArgumentException(
                "Invalid customer name");
        return ledger.get(name).getAmount();
    }

    // checks the income of the company after a certain amount of purchases
    public double income() {
        int size = customers.size();
        // case 1: for one or fewer customers, the company gets all the income
        if (size <= 1) return first * p;
            // case 2: after the first customer, the company only receives half
        else return first * p + (n - first) * p / 2;
    }

    // checks the total amount of products sold by the company
    public int sales() {
        return n;
    }

    // returns record of all unique customer names
    public Iterable<String> record() {
        return customers;
    }

    // checks if an individual was a customer
    public boolean wasCustomer(String name) {
        return customers.contains(name);
    }

    // main method to check functionality of data type
    public static void main(String args[]) {
        Onchain business = new Onchain(100.0);
        Scanner sc = new Scanner(System.in);

        // user begins while loop by giving input "On"
        System.out.println("System: On/Off ");
        String onOff = sc.nextLine();
        if (onOff.equals("On")) System.out.println("To select an option, type its number: ");

        // begin basic user interface to test all methods of Onchain data type, repeatedly
        while (onOff.equals("On")) {
            System.out.println("(1) Purchase | " + "(2) Withdraw Dividend | (3) Check " +
                    "Dividend | (4) Check Purchases | \n(5) Check Company Income | (6) " +
                    "Check Company Sales | (7) Check Customer Record | (8) Finish");

            // use a switch to execute different actions depending on user input
            switch (Integer.parseInt(sc.nextLine())) {
                // purchase a product
                case 1:
                    System.out.println("Customer name: ");
                    String name1 = sc.nextLine();
                    System.out.println("Amount you would like to purchase: ");
                    int quantity = Integer.parseInt(sc.nextLine());
                    business.purchase(name1, quantity);
                    System.out.println();
                    continue;

                    // withdraw dividend, print new dividend balance
                case 2:
                    System.out.println("Customer name: ");
                    String name2 = sc.nextLine();
                    // only execute command if input was valid customer name
                    if (business.wasCustomer(name2)) {
                        System.out.println("Amount to withdraw: ");
                        double withdrawal = Double.parseDouble(sc.nextLine());
                        // check and prevent overdraft
                        if (business.balance(name2) < withdrawal) {
                            System.out.println("Customer " + name2 + " has " +
                                    "over-drafted and the withdrawal has " +
                                    "been cancelled");
                            System.out.println();
                        }
                        // only execute withdrawal if user balance > withdrawal
                        else {
                            business.withdraw(name2, withdrawal);
                            System.out.printf("Your new balance is: $%.2f\n",
                                    business.balance(name2));
                            System.out.println();
                        }
                    } else {
                        System.out.println("Invalid customer name");
                        System.out.println();
                    }
                    continue;

                    // check dividend balance
                case 3:
                    System.out.println("Customer name: ");
                    String name3 = sc.nextLine();
                    // only execute command if input was valid customer name
                    if (business.wasCustomer(name3)) {
                        System.out.printf("Your balance is: $%.2f\n",
                                business.balance(name3));
                        System.out.println();
                    } else {
                        System.out.println("Invalid customer name");
                        System.out.println();
                    }
                    continue;

                    // check amount of products purchased
                case 4:
                    System.out.println("Customer name: ");
                    String name4 = sc.nextLine();
                    // only execute command if input was valid customer name
                    if (business.wasCustomer(name4)) {
                        System.out.println("Your inventory is: " +
                                business.inventory(name4));
                        System.out.println();
                    } else {
                        System.out.println("Invalid customer name");
                        System.out.println();
                    }
                    continue;

                    // check company's total income
                case 5:
                    System.out.printf("The company's total income is: $%.2f\n",
                            business.income());
                    System.out.println();
                    continue;

                    // check company's total sales
                case 6:
                    System.out.println("The company's total sales figure is: "
                            + business.sales());
                    System.out.println();
                    continue;

                    // print record of all customers, their inventories and dividends
                case 7:
                    for (String name : business.record())
                        System.out.println(name + " | " + business.inventory(name) +
                                " | " + business.balance(name));
                    System.out.println();
                    continue;

                    // finish using interface
                case 8:
                    onOff = "Off";
            }
        }
        sc.close();
    }
}
