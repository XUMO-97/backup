package demo;

import com.alibaba.fastjson.JSON;
import com.github.ontio.OntSdk;
import com.github.ontio.account.Account;
import com.github.ontio.common.Address;
import com.github.ontio.common.Helper;
import com.github.ontio.core.transaction.Transaction;
import com.github.ontio.crypto.SignatureScheme;
import com.github.ontio.sdk.exception.SDKException;
import com.github.ontio.sdk.wallet.Identity;
import com.github.ontio.smartcontract.neovm.abi.BuildParams;
//import org.springframework.beans.factory.annotation.Value;

import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

public class OntUtil {

    private static OntSdk ontSdk = null;


    public static String contractAddress = "e1062a3647d27881699b815898fbfc7655d1fa28";
    //public static String contractAddress = "96dd78ea2f6dd85ef2f37c6edfb1663f5bd91175";
    //public static String contractAddress = "f3f3412a7c5680a88c393fbcd591ca3fca2363bc";


    public static void main(String[] args) {

        try {
            OntSdk ont_sdk = OntSdk.getInstance();
            // String ip = "http://polaris1.ont.io";
            String ip = "http://127.0.0.1";
            //        String  ip1 = "http://139.219.139.170";

            // String restUrl = ip + ":" + "20334";
            String rpcUrl = ip + ":" + "20336";
            //        String wsUrl = ip + ":" + "20335";

            ont_sdk.setRpc(rpcUrl);

            ont_sdk.openWalletFile("D:\\ontio\\wallet.dat");
            Account acct1 = ont_sdk.getWalletMgr().getAccount("ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS", "123123");
            String private_key = Helper.toHexString(acct1.serializePrivateKey());

            Account account = new Account(Helper.hexToBytes(private_key), SignatureScheme.SHA256WITHECDSA);
            // "b15963bcc3e2def57f8e2a2c43c088d67ac22972c1a6069ac01a1b6e547574c7"
            // com.github.ontio.account.Account account = ontSdk.getWalletMgr().getAccount("ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS","123123");
            ontSdk = OntSdk.getInstance();
            ontSdk.setConnectPrivateNet();

            List paramList = new ArrayList<>();
            paramList.add("createProperty".getBytes());
            List arg = new ArrayList();
            arg.add(Address.decodeBase58("ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS").toArray());
            List list = new ArrayList();
            List list1 = new ArrayList();
            list1.add(Address.decodeBase58("ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS").toArray());
            list1.add(Long.parseLong("2040004011185674"));
//            2040004011108567;
//            170000000000002
            list.add(list1);
            arg.add(list);
            paramList.add(arg);
            byte[] params = BuildParams.createCodeParamsScript(paramList);
            String result = invokeContract(params, account, 200000000, 50000,false);
            System.out.println(result);


        }catch (Exception e){
            e.printStackTrace();
        }
    }

    public static String invokeContract(byte[] params, Account payerAcct, long gaslimit, long gasprice, boolean preExec) throws Exception{
        if(payerAcct == null){
            throw new SDKException("params should not be null");
        }
        if(gaslimit < 0 || gasprice< 0){
            throw new SDKException("gaslimit or gasprice should not be less than 0");
        }

        Transaction tx = ontSdk.vm().makeInvokeCodeTransaction(Helper.reverse(contractAddress),null,params,payerAcct.getAddressU160().toBase58(),gaslimit,gasprice);

        ontSdk.addSign(tx, payerAcct);
        Object result = null;
        if(preExec) {
            result = ontSdk.getConnect().sendRawTransactionPreExec(tx.toHexString());
        }else {
            result = ontSdk.getConnect().sendRawTransaction(tx.toHexString());
            return tx.hash().toString();
        }

        return result.toString();
    }
}
