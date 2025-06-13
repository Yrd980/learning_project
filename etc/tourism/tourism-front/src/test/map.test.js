import getPosition from "@/util/routeUtil.js";

test("getPosition", async () => {
    await expect(getPosition(121.4737, 31.2304)).resolves.toEqual(
        expect.objectContaining({
            // 这里填入你期望的响应结构
        })
    );
});
