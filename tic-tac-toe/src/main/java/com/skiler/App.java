package com.skiler;

import java.awt.*;
import javax.swing.*;

public class App {
    JFrame frame;
    CardLayout cardLayout;
    JPanel mainPanel;

    // Panels
    JPanel welcomePanel, gamePanel, endPanel;
    JLabel statusLabel;
    JLabel liveScoreLabel; // NEW: Live scoreboard on the main screen!
    JButton[] buttons = new JButton[9];
    boolean playerXTurn = true;

    // Score tracking
    int xWins = 0, oWins = 0, draws = 0;

    // Modern Color Palette
    Color bgDark = new Color(30, 30, 30);
    Color panelDark = new Color(45, 45, 45);
    Color hoverColor = new Color(65, 65, 65);
    Color xColor = new Color(255, 71, 87);  // Neon Red
    Color oColor = new Color(26, 188, 156); // Neon Cyan
    Color winColor = new Color(46, 204, 113); // Success Green

    public App() {
        frame = new JFrame("Tic-Tac-Toe");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(500, 650); // Slightly taller to fit the live scoreboard
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);

        cardLayout = new CardLayout();
        mainPanel = new JPanel(cardLayout);

        createWelcomePanel();
        createGamePanel();
        createEndPanel();

        frame.add(mainPanel);
        frame.setVisible(true);

        cardLayout.show(mainPanel, "Welcome");
    }

    private JButton createStyledButton(String text) {
        JButton button = new JButton(text);
        button.setFocusPainted(false);
        button.setBackground(panelDark);
        button.setForeground(Color.WHITE);
        button.setFont(new Font("Segoe UI", Font.BOLD, 20));
        button.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(80, 80, 80), 1),
            BorderFactory.createEmptyBorder(12, 25, 12, 25)
        ));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));

        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(hoverColor);
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(panelDark);
            }
        });
        return button;
    }

    private void createWelcomePanel() {
        welcomePanel = new JPanel(new BorderLayout(0, 40));
        welcomePanel.setBackground(bgDark);
        welcomePanel.setBorder(BorderFactory.createEmptyBorder(50, 20, 50, 20));

        JLabel title = new JLabel("TIC-TAC-TOE", JLabel.CENTER);
        title.setFont(new Font("Segoe UI", Font.BOLD, 50));
        title.setForeground(Color.WHITE);

        JPanel centerWrapper = new JPanel();
        centerWrapper.setBackground(bgDark);
        JButton startButton = createStyledButton("START GAME");
        startButton.addActionListener(e -> cardLayout.show(mainPanel, "Game"));
        centerWrapper.add(startButton);

        welcomePanel.add(title, BorderLayout.CENTER);
        welcomePanel.add(centerWrapper, BorderLayout.SOUTH);

        mainPanel.add(welcomePanel, "Welcome");
    }

    private void createGamePanel() {
        gamePanel = new JPanel(new BorderLayout(0, 20));
        gamePanel.setBackground(bgDark);
        gamePanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        // --- THE NEW LIVE SCOREBOARD HEADER ---
        JPanel topHeader = new JPanel(new GridLayout(2, 1, 0, 5));
        topHeader.setBackground(bgDark);

        statusLabel = new JLabel("Player X's Turn", JLabel.CENTER);
        statusLabel.setFont(new Font("Segoe UI", Font.BOLD, 28));
        statusLabel.setForeground(xColor);

        liveScoreLabel = new JLabel("X: 0  |  O: 0  |  Draws: 0", JLabel.CENTER);
        liveScoreLabel.setFont(new Font("Segoe UI", Font.BOLD, 16));
        liveScoreLabel.setForeground(new Color(150, 150, 150));

        topHeader.add(statusLabel);
        topHeader.add(liveScoreLabel);
        gamePanel.add(topHeader, BorderLayout.NORTH);

        JPanel boardPanel = new JPanel(new GridLayout(3, 3, 10, 10));
        boardPanel.setBackground(bgDark);
        
        for (int i = 0; i < 9; i++) {
            buttons[i] = new JButton("");
            buttons[i].setFont(new Font("Segoe UI", Font.BOLD, 90));
            buttons[i].setBackground(panelDark);
            buttons[i].setFocusPainted(false);
            buttons[i].setBorder(BorderFactory.createLineBorder(new Color(60, 60, 60), 1));
            buttons[i].setCursor(new Cursor(Cursor.HAND_CURSOR));
            
            final int index = i;
            buttons[i].addActionListener(e -> handleMove(index));
            boardPanel.add(buttons[i]);
        }
        gamePanel.add(boardPanel, BorderLayout.CENTER);

        JPanel bottomWrapper = new JPanel();
        bottomWrapper.setBackground(bgDark);
        JButton restartButton = createStyledButton("Reset Board");
        restartButton.addActionListener(e -> resetBoard());
        bottomWrapper.add(restartButton);
        
        gamePanel.add(bottomWrapper, BorderLayout.SOUTH);

        mainPanel.add(gamePanel, "Game");
    }

    private void createEndPanel() {
        endPanel = new JPanel(new BorderLayout(0, 30));
        endPanel.setBackground(bgDark);
        endPanel.setBorder(BorderFactory.createEmptyBorder(50, 20, 50, 20));

        JLabel scoreLabel = new JLabel("", JLabel.CENTER);
        scoreLabel.setFont(new Font("Segoe UI", Font.PLAIN, 24));
        scoreLabel.setForeground(Color.LIGHT_GRAY);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 0));
        buttonPanel.setBackground(bgDark);

        JButton playAgainButton = createStyledButton("Play Again");
        playAgainButton.addActionListener(e -> {
            resetBoard();
            cardLayout.show(mainPanel, "Game");
        });

        JButton exitButton = createStyledButton("Exit");
        exitButton.addActionListener(e -> System.exit(0));

        buttonPanel.add(playAgainButton);
        buttonPanel.add(exitButton);

        endPanel.add(scoreLabel, BorderLayout.CENTER);
        endPanel.add(buttonPanel, BorderLayout.SOUTH);

        endPanel.putClientProperty("scoreLabel", scoreLabel);
        
        // THE BUG FIX: I forgot this exact line in the last code!
        mainPanel.add(endPanel, "End");
    }

    private void handleMove(int index) {
        if (buttons[index].getText().equals("")) {
            if (playerXTurn) {
                buttons[index].setForeground(xColor);
                buttons[index].setText("X");
                statusLabel.setText("Player O's Turn");
                statusLabel.setForeground(oColor);
            } else {
                buttons[index].setForeground(oColor);
                buttons[index].setText("O");
                statusLabel.setText("Player X's Turn");
                statusLabel.setForeground(xColor);
            }
            playerXTurn = !playerXTurn;
            checkWin();
        }
    }

    private void checkWin() {
        int[][] winConditions = {
            {0,1,2},{3,4,5},{6,7,8},
            {0,3,6},{1,4,7},{2,5,8},
            {0,4,8},{2,4,6}
        };

        for (int[] condition : winConditions) {
            String b1 = buttons[condition[0]].getText();
            String b2 = buttons[condition[1]].getText();
            String b3 = buttons[condition[2]].getText();

            if (!b1.equals("") && b1.equals(b2) && b2.equals(b3)) {
                declareWinner(b1, condition);
                return;
            }
        }

        boolean full = true;
        for (JButton b : buttons) {
            if (b.getText().equals("")) {
                full = false;
                break;
            }
        }
        if (full) {
            draws++;
            updateLiveScore(); // Update the live board immediately
            showEndPanel("It's a Draw!", false);
        }
    }

    private void declareWinner(String winner, int[] winLine) {
        if (winner.equals("X")) xWins++;
        else oWins++;
        
        updateLiveScore(); // Update the live board immediately

        statusLabel.setText(winner + " WINS!");
        statusLabel.setForeground(winColor);

        // Highlight the winning row
        for (int i : winLine) {
            buttons[i].setBackground(winColor);
            buttons[i].setForeground(bgDark); 
        }

        // Lock the board
        for (JButton b : buttons) {
            b.setEnabled(false);
        }

        // The 1.5 second pause before showing the third panel!
        Timer timer = new Timer(1500, e -> showEndPanel(winner + " Wins!", true));
        timer.setRepeats(false);
        timer.start();
    }

    private void updateLiveScore() {
        liveScoreLabel.setText("X: " + xWins + "  |  O: " + oWins + "  |  Draws: " + draws);
    }

    private void showEndPanel(String resultTitle, boolean someoneWon) {
        JLabel scoreLabel = (JLabel) endPanel.getClientProperty("scoreLabel");
        
        String titleHtml = someoneWon ? "<h1 style='color:#2ecc71; font-size: 36px; margin-bottom: 20px;'>" + resultTitle + "</h1>" 
                                      : "<h1 style='color:#f1c40f; font-size: 36px; margin-bottom: 20px;'>" + resultTitle + "</h1>";
        
        scoreLabel.setText("<html><center>" + titleHtml + 
                           "<table style='font-size: 20px; color: white;'>" +
                           "<tr><td style='color:#ff4757;'>Player X Wins:</td><td>&nbsp;" + xWins + "</td></tr>" +
                           "<tr><td style='color:#1abc9c;'>Player O Wins:</td><td>&nbsp;" + oWins + "</td></tr>" +
                           "<tr><td style='color:#95a5a6;'>Draws:</td><td>&nbsp;" + draws + "</td></tr>" +
                           "</table></center></html>");
        cardLayout.show(mainPanel, "End");
    }

    private void resetBoard() {
        for (JButton b : buttons) {
            b.setText("");
            b.setBackground(panelDark);
            b.setEnabled(true);
        }
        playerXTurn = true;
        statusLabel.setText("Player X's Turn");
        statusLabel.setForeground(xColor);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(App::new);
    }
}