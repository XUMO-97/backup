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


    public static String contractAddress = "19cda29c53223b2818a8a16cc9ac9ae8c914f1af";
    //public static String contractAddress = "96dd78ea2f6dd85ef2f37c6edfb1663f5bd91175";
    //public static String contractAddress = "f3f3412a7c5680a88c393fbcd591ca3fca2363bc";


    public static void main(String[] args) {

        try {
            Account account = new Account(Helper.hexToBytes("520ccdc87c6d0f6b5cbbcb6a873ada61ea816703f85e908b7f921cbc4200b4a7"), SignatureScheme.SHA256WITHECDSA);

            ontSdk = OntSdk.getInstance();
            ontSdk.setConnectTestNet();

            List paramList = new ArrayList<>();
            paramList.add("createProperty".getBytes());
            List arg = new ArrayList();
            arg.add(Address.decodeBase58("AUqmCH5Y5qHgLmzK1tbTooNo5nhTbmbA22").toArray());
            List list = new ArrayList();
            List list1 = new ArrayList();
            list1.add(Address.decodeBase58("AUqmCH5Y5qHgLmzK1tbTooNo5nhTbmbA22").toArray());
            list1.add(Long.parseLong("204000401118567"));
//            2040004011108567;
//            170000000000002
            list.add(list1);
            arg.add(list);
            paramList.add(arg);
            byte[] params = BuildParams.createCodeParamsScript(paramList);
            String result = invokeContract(params, account, 20000, 500,false);
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
