package org.tron.studio.ui;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.jfoenix.controls.*;
import de.jensd.fx.glyphs.materialdesignicons.MaterialDesignIconView;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.input.Clipboard;
import javafx.scene.input.ClipboardContent;
import javafx.scene.input.MouseEvent;
import javafx.scene.control.TextArea;
import javafx.scene.input.MouseButton;
import javafx.scene.layout.ColumnConstraints;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import org.apache.commons.lang3.StringUtils;
import org.controlsfx.control.Notifications;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.spongycastle.util.encoders.Hex;
import org.tron.abi.FunctionEncoder;
import org.tron.abi.TypeReference;
import org.tron.abi.datatypes.Function;
import org.tron.abi.datatypes.Type;
import org.tron.abi.datatypes.generated.AbiTypes;
import org.tron.api.GrpcAPI.TransactionExtention;
import org.tron.core.Wallet;
import org.tron.core.capsule.TransactionCapsule;
import org.tron.core.services.http.Util;
import org.tron.protos.Protocol.Transaction;
import org.tron.studio.ShareData;
import org.tron.studio.TransactionHistoryItem;
import org.tron.studio.solc.CompilationResult;
import org.tron.studio.solc.CompilationResult.ContractMetadata;
import org.tron.studio.solc.SolidityCompiler;
import org.tron.studio.utils.AbiUtil;
import org.tron.studio.walletserver.WalletClient;

import java.io.IOException;
import java.net.URL;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RightTabRunController implements Initializable {

    static final Logger logger = LoggerFactory.getLogger(RightTabRunController.class);
    private static String DEFAULT_FEE_LIMIT = String.valueOf(100);
    private static String DEFAULT_VALUE = String.valueOf(0);
    private static String DEFAULT_RATIO = String.valueOf(100);
    public JFXComboBox<String> environmentComboBox;
    public JFXComboBox<String> contractComboBox;
    public JFXComboBox<String> accountComboBox;
    public JFXTextField feeLimitTextField;
    public JFXTextField valueTextField;
    public JFXTextField tokenIdTextField;
    public JFXTextField tokenValueTextField;
    public JFXComboBox<String> feeUnitComboBox;
    public JFXComboBox<String> valueUnitComboBox;
    public JFXTextField userPayRatio;
    public JFXListView deployedContractList;
    public JFXTextField constructorParaTextField;
    public JFXTextField current_ip_port = new JFXTextField();
    private boolean isDeploying;

    public void initialize(URL location, ResourceBundle resources) {
        isDeploying = false;

        environmentComboBox.setItems(FXCollections.observableArrayList(
            ShareData.saved_network.keySet()
        ));
        environmentComboBox.setValue(ShareData.currentEnvironment);
        this.current_ip_port.setText(ShareData.currentRpcIp + ":" + String.valueOf(ShareData.currentRpcPort));
        this.current_ip_port.setDisable(true);

        ShareData.newNetwork.addListener((observable, oldValue, newValue) -> {
            environmentComboBox.getItems().clear();
            environmentComboBox.setItems(FXCollections.observableArrayList(ShareData.saved_network.keySet()));
            environmentComboBox.setValue(ShareData.currentEnvironment);
        });
        ShareData.newNetwork.set(ShareData.currentEnvironment);
        environmentComboBox.getSelectionModel().selectedItemProperty().addListener((observable, oldValue, newValue) -> {
            if (StringUtils.isNotEmpty(newValue)) {
                ShareData.currentEnvironment = newValue.trim();
                ShareData.currentRpcIp = ShareData.saved_network.get(newValue).url.trim();
                ShareData.currentRpcPort = ShareData.saved_network.get(newValue).port;
                this.current_ip_port.setText(ShareData.currentRpcIp + ":" + String.valueOf(ShareData.currentRpcPort));
                this.current_ip_port.setDisable(true);
            }

        });


        ShareData.newAccount.addListener((observable, oldValue, newValue) -> {
            accountComboBox.getItems().clear();
            accountComboBox.setItems(FXCollections.observableArrayList(ShareData.testAccount.keySet()));
            accountComboBox.getSelectionModel().selectFirst();
        });
        ShareData.newAccount.set(ShareData.testAccount.keySet().stream().findFirst().get());
        accountComboBox.getSelectionModel().selectedItemProperty().addListener((observable, oldValue, newValue) -> {
            if (StringUtils.isNotEmpty(newValue)) {
                ShareData.wallet = new WalletClient(Hex.decode(ShareData.testAccount.get(newValue)));
            }
        });


        feeUnitComboBox.setItems(FXCollections.observableArrayList(
                "trx",
                "sun"
        ));
        feeUnitComboBox.getSelectionModel().selectFirst();

        valueUnitComboBox.setItems(FXCollections.observableArrayList(
                "trx",
                "sun"
        ));
        valueUnitComboBox.getSelectionModel().selectFirst();

        feeLimitTextField.setText(DEFAULT_FEE_LIMIT);
        valueTextField.setText(DEFAULT_VALUE);
        tokenIdTextField.setText(DEFAULT_VALUE);
        tokenValueTextField.setText(DEFAULT_VALUE);
        userPayRatio.setText(DEFAULT_RATIO);

        reloadContract();

        ShareData.currentSolidityCompilerResult.addListener((observable, oldValue, solidityCompilerResult) -> {

                }
        );


    }

    private void reloadContract() {
        ShareData.currentSolidityCompilerResult.addListener((observable, oldValue, solidityCompilerResult) -> {
            if (solidityCompilerResult == null) {
                return;
            }
            List<String> contractNameList = new ArrayList<>();
            CompilationResult compilationResult;
            try {
                compilationResult = CompilationResult.parse(solidityCompilerResult.output);
            } catch (IOException e) {
                logger.error("Failed to parse compile result {}", e);
                return;
            }
            compilationResult.getContracts().forEach(contractResult -> {
                JSONObject metaData = JSON.parseObject(contractResult.metadata);
                if (metaData == null) {
                    return;
                }
                JSONObject compilationTarget = metaData.getJSONObject("settings")
                        .getJSONObject("compilationTarget");
                compilationTarget.forEach((sol, value) -> {
                    contractNameList.add((String) value);
                });
            });
            contractComboBox.setItems(FXCollections.observableArrayList(
                    contractNameList
            ));
            contractComboBox.getSelectionModel().selectFirst();
        });

    }

    public void onClickDeploy(ActionEvent actionEvent) {
        if (isDeploying) {
            return;
        }
        isDeploying = true;
        String currentContractName = contractComboBox.valueProperty().get();
        ShareData.currentContractName.set(currentContractName);
        ShareData.currentAccount = accountComboBox.valueProperty().get();
        ShareData.currentValue = valueTextField.getText();
        ShareData.currentTokenId = tokenIdTextField.getText();
        ShareData.currentTokenValue = tokenValueTextField.getText();

        SolidityCompiler.Result solidityCompileResult = ShareData.getSolidityCompilerResult(ShareData.currentContractFileName.get());
        CompilationResult compilationResult = null;
        try {
            compilationResult = CompilationResult.parse(solidityCompileResult.output);
        } catch (Exception e) {
            String uuid = UUID.randomUUID().toString();
            addTransactionHistoryItem(uuid, new TransactionHistoryItem(
                    TransactionHistoryItem.Type.InfoString,
                    "Not ready to parse compile result {} " + e.getMessage(),
                    null));
            isDeploying = false;
            return;
        }

        if (compilationResult == null) {
            logger.error("No CompilationResult found");
            isDeploying = false;
            return;
        }

        ContractMetadata currentContractFileMetadata = compilationResult.getContract(currentContractName);

        final boolean[] deployContractResult = {false};
        StringBuilder bin = new StringBuilder(currentContractFileMetadata.bin);

        try {
            //Find out constructor, and encode constructor parameter, then append it to the end of bytecode
            List<JSONObject> abiJson = JSONArray.parseArray(currentContractFileMetadata.abi, JSONObject.class);
            Optional<JSONObject> constructorJSONObject = abiJson.stream()
                    .filter(entry -> StringUtils.equalsIgnoreCase("constructor", entry.getString("type")))
                    .findFirst();
            if (constructorJSONObject.isPresent()) {
                JSONObject constructorJSON = constructorJSONObject.get();
                JSONArray inputsArray = constructorJSON.getJSONArray("inputs");
                List<String> constructorParaValue = Arrays
                        .asList(constructorParaTextField.getText().split(","));
                if (!inputsArray.isEmpty()) {
                    List<Type> constructorPara = new ArrayList<>();
                    for (int i = 0; i < inputsArray.size(); i++) {
                        JSONObject inputType = inputsArray.getJSONObject(i);
                        String value = i < constructorParaValue.size() ? constructorParaValue.get(i) : "0";
                        value = StringUtils.isNoneEmpty(value) ? value : "0";
                        Type tp = AbiTypes.getTypeWithValue(inputType.getString("type"), value);
                        constructorPara.add(tp);
                    }
                    String encodedConstructor = FunctionEncoder.encodeConstructor(constructorPara);
                    bin.append(encodedConstructor);
                }
            }
        } catch (Exception e) {
            String uuid = UUID.randomUUID().toString();
            addTransactionHistoryItem(uuid, new TransactionHistoryItem(
                    TransactionHistoryItem.Type.InfoString,
                    "Failed to deployContract. " + e.getMessage(),
                    null));
            logger.error("Failed to deployContract {}", e);
            isDeploying = false;
            return;
        }

        {   // GONNA ADD OVERFLOW CHECK LATER
            long callValue = Long.parseLong(valueTextField.getText());
            long tokenId = Long.parseLong(tokenIdTextField.getText());
            long tokenValue = Long.parseLong(tokenValueTextField.getText());
            if (callValue < 0) {
                Notifications note = Notifications.create().title("Trigger Contract Failed").text("Call value should be equal or greater than 0");
                note.show();
                return;
            }
            if (valueUnitComboBox.getSelectionModel().getSelectedIndex() == 0) {
                callValue *= ShareData.TRX_SUN_UNIT;
            }

            long feeLimit = Long.parseLong(feeLimitTextField.getText());

            if (feeUnitComboBox.getSelectionModel().getSelectedIndex() == 0) {
                feeLimit *= ShareData.TRX_SUN_UNIT;
            }
            if (feeLimit < 0 || feeLimit > 1000 * ShareData.TRX_SUN_UNIT) {
                Notifications note = Notifications.create().title("Trigger Contract Failed").text("Fee limit should between 0 and 1000 trx or 1E9 Sun");
                note.show();
                return;
            }

            long finalFeeLimit = feeLimit;
            long finalCallValue = callValue;
            String byteCode = bin.toString();

            try {
                if (hasLibrary(byteCode)) {
                    byteCode = deployLibrary(compilationResult, currentContractName, byteCode, finalFeeLimit);
                }
                deployContractResult[0] = ShareData.wallet
                        .deployContract(currentContractName, currentContractFileMetadata.abi, byteCode,
                                finalFeeLimit, finalCallValue,
                                Long.parseLong(userPayRatio.getText()), tokenId, tokenValue, null);

            } catch (Exception e) {
                String uuid = UUID.randomUUID().toString();
                addTransactionHistoryItem(uuid, new TransactionHistoryItem(
                        TransactionHistoryItem.Type.InfoString,
                        "Failed to deployContract. " + e.getMessage(),
                        null));
                logger.error("Failed to deployContract {}", e);
                isDeploying = false;
                return;
            }
        }

        if (!deployContractResult[0]) {
            String uuid = UUID.randomUUID().toString();
            addTransactionHistoryItem(uuid, new TransactionHistoryItem(
                    TransactionHistoryItem.Type.InfoString,
                    "Failed to deployContract. Please try again",
                    null));
            isDeploying = false;
            return;
        }

        TransactionExtention transactionExtention = ShareData.wallet.getLastTransactionExtention();
        String transactionId = Hex.toHexString(transactionExtention.getTxid().toByteArray());
        if (!transactionExtention.getResult().getResult()) {
            addTransactionHistoryItem(transactionId, new TransactionHistoryItem(
                    TransactionHistoryItem.Type.InfoString,
                    String.format("Unable to get last TransactionExtention: %s",
                            transactionExtention.getResult().getMessage().toStringUtf8()),
                    null));
            isDeploying = false;
            return;
        }

        Transaction transaction = ShareData.wallet.getLastTransaction();
        transactionId = Hex.toHexString(new TransactionCapsule(transaction).getTransactionId().getBytes());
        addTransactionHistoryItem(transactionId, new TransactionHistoryItem(TransactionHistoryItem.Type.Transaction, transaction, null));

        ShareData.currentContractName.set(currentContractName);

        byte[] ownerAddress = Wallet.decodeFromBase58Check(accountComboBox.getSelectionModel().getSelectedItem());
        byte[] contractAddress = Util.generateContractAddress(transaction, ownerAddress);
        deployedContractList.getItems()
                .add(getContractRunPanel(currentContractName, contractAddress, currentContractFileMetadata.abi));
        isDeploying = false;
    }


    private JFXListView getContractRunPanel(String contractName, byte[] contractAddress, String abi) {
        JFXListView listView = new JFXListView();
        listView.getStyleClass().add("sublist");

        HBox title = new HBox();
        String contractAddressString = Wallet.encode58Check(contractAddress);
        Label transactionLabel = new Label(String.format("%s %s", contractName, contractAddressString));

        MaterialDesignIconView copyIcon = new MaterialDesignIconView();
        copyIcon.setGlyphName("CONTENT_COPY");
        copyIcon.setStyleClass("icon");
        JFXRippler jfxRippler = new JFXRippler();
        jfxRippler.getStyleClass().add("icons-rippler1");
        jfxRippler.setPosition(JFXRippler.RipplerPos.BACK);
        jfxRippler.getChildren().add(copyIcon);
        jfxRippler.setOnMouseClicked(event -> {
            Clipboard clipboard = Clipboard.getSystemClipboard();
            ClipboardContent clipboardContent = new ClipboardContent();
            clipboardContent.putString(contractAddressString);
            clipboard.setContent(clipboardContent);
            Notifications note = Notifications.create().title("Copy Contract Address").text(contractAddressString);
            note.show();
        });

        title.getChildren().add(transactionLabel);
        title.getChildren().add(jfxRippler);
        listView.setGroupnode(title);

        List<String> abiJson = JSONArray.parseArray(abi, String.class);
        GridPane gridPane = new GridPane();
        gridPane.setHgap(5);
        gridPane.setVgap(5);
        ColumnConstraints columnConstraints0 = new ColumnConstraints();
        columnConstraints0.setHgrow(Priority.NEVER);
        ColumnConstraints columnConstraints1 = new ColumnConstraints();
        columnConstraints1.setHgrow(Priority.ALWAYS);
        gridPane.getColumnConstraints().add(columnConstraints0);
        gridPane.getColumnConstraints().add(columnConstraints1);
        int index = 0;
        for (String entry : abiJson) {
            JSONObject entryJson = JSONObject.parseObject(entry);
            if (StringUtils.equalsIgnoreCase("function", entryJson.getString("type"))) {
                JFXButton functionButton = new JFXButton(entryJson.getString("name"));
                if (entryJson.getBoolean("constant")) {
                    functionButton.getStyleClass().add("custom-jfx-button-raised-fix-width2");
                } else {
                    functionButton.getStyleClass().add("custom-jfx-button-raised-fix-width");
                }

                JFXTextField parameterText = new JFXTextField();
                gridPane.add(functionButton, 0, index);
                gridPane.add(parameterText, 1, index);

                JSONArray inputsJsonArray = entryJson.getJSONArray("inputs");
                JSONArray outputsJsonArray = entryJson.getJSONArray("outputs");
                StringBuilder parameterPromot = new StringBuilder();

                StringBuilder methodStr = new StringBuilder(entryJson.getString("name"));
                methodStr.append("(");
                if (inputsJsonArray != null && inputsJsonArray.size() > 0) {
                    for (int j = 0; j < inputsJsonArray.size(); j++) {
                        JSONObject inputItem = inputsJsonArray.getJSONObject(j);
                        String inputName = inputItem.getString("name");
                        String type = inputItem.getString("type");
                        parameterPromot.append(type).append(" ").append(inputName);
                        methodStr.append(type);
                        if (j != inputsJsonArray.size() - 1) {
                            parameterPromot.append(", ");
                            methodStr.append(",");
                        }
                    }
                } else {
                    parameterText.setVisible(false);
                }

                List<TypeReference<?>> outputParaList = new ArrayList<>();
                if (outputsJsonArray != null && outputsJsonArray.size() > 0) {
                    for (int j = 0; j < outputsJsonArray.size(); j++) {
                        JSONObject outputItem = outputsJsonArray.getJSONObject(j);
                        String type = outputItem.getString("type");
                        outputParaList.add(AbiTypes.getTypeReference(type, false));
                    }
                }
                Function functionForReturn = new Function(entryJson.getString("name"),
                        Collections.emptyList(), outputParaList);
                methodStr.append(")");
                parameterText.setPromptText(parameterPromot.toString());
                functionButton.setOnAction(new ClickTriggerAction(contractAddress, methodStr.toString(), functionForReturn, parameterText));
            }
            index++;
        }
        listView.getItems().add(gridPane);
        return listView;
    }

    private void addTransactionHistoryItem(String id, TransactionHistoryItem item) {

        String currentContractName = ShareData.currentContractName.get();
        String transactionHeadMsg = String.format("creation of %s pending...", currentContractName);
        UUID uuid = UUID.randomUUID();
        ShareData.transactionHistory.put(uuid.toString(), new TransactionHistoryItem(TransactionHistoryItem.Type.InfoString, transactionHeadMsg, null));
        ShareData.addTransactionAction.set(uuid.toString());

        new Thread(() -> {
            try {
                if (item.getType() == TransactionHistoryItem.Type.Transaction) {
                    Thread.sleep(3000);
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            Platform.runLater(() -> {
                ShareData.transactionHistory.put(id, item);
                ShareData.addTransactionAction.set(id);
            });
        }).start();
    }

    private boolean hasLibrary(String byteCode) {
        if (StringUtils.isEmpty(byteCode.trim())) {
            return false;
        }
        return byteCode.matches(".*__.*__.*");
    }

    private Set<String> getMatchers(String regex, String source) {
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(source);
        Set<String> set = new HashSet<>();
        while (matcher.find()) {
            set.add(matcher.group());
        }
        return set;
    }

    private String deployLibrary(CompilationResult compilationResult, String currentContractName, String byteCode, long finalFeeLimit) {
        Map<String, String> libraryDeployedAddress = new HashMap<>();
        Set<String> usedLibrarySet = getMatchers("(__.*?_*__)", byteCode);
        for (String usedLibrary : usedLibrarySet) {
            String libraryContractName = getMatchers(".*[a-zA-Z0-9]", usedLibrary).stream().findFirst().get().split(":")[1];
            ContractMetadata libraryMetadata = compilationResult.getContract(libraryContractName);
            try {
                boolean deployLibraryResult = ShareData.wallet
                        .deployContract(currentContractName, libraryMetadata.abi, libraryMetadata.bin,
                                finalFeeLimit, 0,
                                Long.parseLong(userPayRatio.getText()), 0, 0, null);
                if (!deployLibraryResult) {
                    logger.error("Failed to deployed library {}", libraryContractName);
                } else {
                    Transaction lastTransaction = ShareData.wallet.getLastTransaction();
                    byte[] ownerAddress = Wallet.decodeFromBase58Check(accountComboBox.getSelectionModel().getSelectedItem());
                    byte[] contractAddress = Util.generateContractAddress(lastTransaction, ownerAddress);
                    libraryDeployedAddress.put(usedLibrary, Hex.toHexString(contractAddress));
                }
            } catch (Exception e) {
                logger.error("Failed to deployed library {} {}", libraryContractName, e);
            }
        }
        final String[] returnByteCode = {byteCode};
        libraryDeployedAddress.forEach((libraryName, address) -> {
            String libraryAddress = address.substring(2);
            returnByteCode[0] = returnByteCode[0].replace(libraryName, libraryAddress);
        });
        return returnByteCode[0];
    }

    public void onClickClear(MouseEvent actionEvent) {
        deployedContractList.getItems().clear();
    }

    public void onClickAddAddress(MouseEvent mouseEvent) {
        logger.debug("onClickAddAddress");
    }

    public void onClickCopyAddress(MouseEvent mouseEvent) {
        Clipboard clipboard = Clipboard.getSystemClipboard();
        ClipboardContent clipboardContent = new ClipboardContent();
        clipboardContent.putString(accountComboBox.valueProperty().get());
        clipboard.setContent(clipboardContent);
    }

    public void onClickRefresh(MouseEvent mouseEvent){
        this.current_ip_port.setText(ShareData.currentRpcIp + ":" + String.valueOf(ShareData.currentRpcPort));
    }

    class ClickTriggerAction implements EventHandler<ActionEvent> {

        byte[] contractAddress;
        String methodStr;
        JFXTextField parameterText;
        Function function;

        public ClickTriggerAction(byte[] contractAddress, String methodStr, Function function, JFXTextField parameterText) {
            this.contractAddress = contractAddress;
            this.methodStr = methodStr;
            this.parameterText = parameterText;
            this.function = function;
        }

        @Override
        public void handle(ActionEvent event) {
            long callValue = Long.parseLong(valueTextField.getText());
            if (valueUnitComboBox.getSelectionModel().getSelectedIndex() == 0) {
                callValue *= ShareData.TRX_SUN_UNIT;
            }
            long feeLimit = Long.parseLong(feeLimitTextField.getText());
            if (feeUnitComboBox.getSelectionModel().getSelectedIndex() == 0) {
                feeLimit *= ShareData.TRX_SUN_UNIT;
            }
            try {
                byte[] data = Hex.decode(AbiUtil.parseMethod(methodStr, parameterText.getText().trim(), false));
                ShareData.wallet.triggerContract(contractAddress, callValue, data, feeLimit);
                processTriggerContractResult();
            } catch (Exception e) {
                Notifications note = Notifications.create().title("Trigger Contract Failed").text(e.getMessage());
//                addTransactionHistoryItem("Error", new TransactionHistoryItem())
                note.show();
            }
        }

        private void processTriggerContractResult() {
            TransactionExtention transactionExtention = ShareData.wallet.getLastTransactionExtention();
            String transactionId = Hex.toHexString(transactionExtention.getTxid().toByteArray());
            if (!transactionExtention.getResult().getResult()) {
                addTransactionHistoryItem(transactionId, new TransactionHistoryItem(
                        TransactionHistoryItem.Type.InfoString,
                        String.format("Unable to get last TransactionExtention: %s",
                                transactionExtention.getResult().getMessage().toStringUtf8()),
                        null
                ));
                return;
            }

            if (transactionExtention.getConstantResultCount() > 0) {
                addTransactionHistoryItem(transactionId, new TransactionHistoryItem(TransactionHistoryItem.Type.TransactionExtension, transactionExtention, function));
                return;
            }
            Transaction transaction = ShareData.wallet.getLastTransaction();
            transactionId = Hex.toHexString(new TransactionCapsule(transaction).getTransactionId().getBytes());
            addTransactionHistoryItem(transactionId, new TransactionHistoryItem(TransactionHistoryItem.Type.Transaction, transaction, function));
        }
    }


}